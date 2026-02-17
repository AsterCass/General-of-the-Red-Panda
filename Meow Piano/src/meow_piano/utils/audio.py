import os
import threading
import numpy as np
import sounddevice as sd
import soundfile as sf


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
        print("Loading samples...")

        global_peak = 0

        # 先读一遍找最大峰值
        for file in os.listdir(self.sample_folder):
            if file.endswith(".wav"):
                path = os.path.join(self.sample_folder, file)
                data, sr = sf.read(path, dtype="float32")

                if sr != self.samplerate:
                    raise ValueError(f"{file} 采样率不一致")

                peak = np.max(np.abs(data))
                if peak > global_peak:
                    global_peak = peak

        # 再加载并统一标准化
        for file in os.listdir(self.sample_folder):
            if file.endswith(".wav"):
                note = file.replace(".wav", "")
                path = os.path.join(self.sample_folder, file)
                data, _ = sf.read(path, dtype="float32")

                if data.ndim > 1:
                    data = data.mean(axis=1)  # 转单声道

                if global_peak > 0:
                    data = data / global_peak

                self.samples[note] = data

        print(f"Loaded {len(self.samples)} samples.")


    # 播放接口
    def note_on(self, note):
        if note not in self.samples:
            return

        with self.lock:
            if len(self.active_notes) >= self.max_polyphony:
                self.active_notes.pop(0)

            self.active_notes.append({
                "data": self.samples[note],
                "pos": 0
            })


    # 音频回调
    def _audio_callback(self, out_data, frames, time, status):
        buffer = np.zeros(frames, dtype=np.float32)

        with self.lock:
            finished = []

            for note in self.active_notes:
                start = note["pos"]
                end = start + frames
                data = note["data"]

                if start < len(data):
                    chunk = data[start:end]
                    buffer[:len(chunk)] += chunk
                    note["pos"] += frames
                else:
                    finished.append(note)

            for note in finished:
                self.active_notes.remove(note)

        # 防止爆音 clipping
        buffer = np.clip(buffer, -1.0, 1.0)

        out_data[:] = buffer.reshape(-1, 1)


    # 启动音频流
    def _start_stream(self):
        self.stream = sd.OutputStream(
            samplerate=self.samplerate,
            channels=1,
            callback=self._audio_callback,
            blocksize=128,
            latency="low",
            dtype="float32"
        )
        self.stream.start()


    # 关闭
    def close(self):
        self.stream.stop()
        self.stream.close()
