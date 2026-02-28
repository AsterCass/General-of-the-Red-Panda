import os
import threading

import numpy as np
import sounddevice as sd
import soundfile as sf
from loguru import logger


class AudioEngine:
    def __init__(self, sample_folder="samples", samplerate=44100, max_polyphony=32):
        self.sample_folder = sample_folder
        self.samplerate = samplerate
        self.max_polyphony = max_polyphony

        self.samples = {}
        self.active_notes = []
        self.lock = threading.Lock()

        self._load_samples()
        self._start_stream()

    # 预加载 + 标准化
    def _load_samples(self):
        raw = {}
        global_peak = 0

        for file in os.listdir(self.sample_folder):
            if file.endswith(".wav"):
                path = os.path.join(self.sample_folder, file)
                data, sr = sf.read(path, dtype="float32")

                if sr != self.samplerate:
                    raise ValueError("Inconsistent sampling rate")

                if data.ndim > 1:
                    data = data.mean(axis=1)

                peak = np.max(np.abs(data))
                global_peak = max(global_peak, peak)

                raw[file.replace(".wav", "")] = data

        for note, data in raw.items():
            if global_peak > 0:
                data = data / global_peak
            self.samples[int(note)] = data

        logger.info(f"Loaded {len(self.samples)} samples.")


    # 播放接口
    def note_on(self, note, velocity=50):
        if note not in self.samples:
            return
        gain = (velocity / 127.0) ** 1.4

        with self.lock:
            if len(self.active_notes) >= self.max_polyphony:
                self.active_notes.pop(0)

            self.active_notes.append({
                "data": self.samples[note],
                "pos": 0,
                "gain": gain
            })


    # 音频回调
    def _audio_callback(self, out_data, frames, time, status):
        buffer = np.zeros(frames, dtype=np.float32)

        notes = self.active_notes[:]  # 不加锁读取

        still_active = []

        for note in notes:
            start = note["pos"]
            end = start + frames
            data = note["data"]

            if start >= len(data):
                continue

            chunk = data[start:end] * note["gain"]
            buffer[:len(chunk)] += chunk
            note["pos"] += len(chunk)

            if note["pos"] < len(data):
                still_active.append(note)

        self.active_notes = still_active

        # soft clip
        # 1.平滑压缩，超出部分渐变，但是稍慢，而且融音不太好
        buffer = np.tanh(buffer)
        out_data[:, 0] = buffer
        # 2.按音符数缩放，避免后加入的音压制先加入的，融音效果最好，但是听起来怪怪的
        # n = max(len(still_active), 1)
        # buffer *= (1.0 / np.sqrt(n))
        # buffer /= (1.0 + np.abs(buffer))
        # out_data[:, 0] = buffer
        # 3. 同时播放多个可能会有爆音，但是融音效果稍好，速度快
        # buffer *= 0.8 # 防止爆音
        # np.clip(buffer, -1, 1, out=buffer)
        # out_data[:, 0] = buffer


    # 启动音频流
    def _start_stream(self):
        self.stream = sd.OutputStream(
            samplerate=self.samplerate,
            channels=1,
            callback=self._audio_callback,
            blocksize=32,
            latency=0.075,
            dtype="float32",
        )
        self.stream.start()


    # 关闭
    def close(self):
        self.stream.stop()
        self.stream.close()
