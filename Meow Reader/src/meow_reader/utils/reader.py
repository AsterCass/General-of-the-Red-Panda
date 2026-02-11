import threading
import time
from pathlib import Path

import numpy as np
import sounddevice as sd
from loguru import logger
from piper import PiperVoice


class Reader:
    """
    # https://github.com/rhasspy/piper
    # https://github.com/OHF-Voice/piper1-gpl
    # https://huggingface.co/rhasspy/piper-voices
    # python -m piper.download_voices en_US-lessac-medium
    """

    def __init__(self, model_path: Path):
        if not model_path.is_file():
            raise FileNotFoundError(f"模型文件不存在: {model_path}")

        self.voice = PiperVoice.load(model_path)
        logger.info(f"模型加载成功：{model_path.name}")

        # 当前要播放的文本
        self._current_text = None
        # 中断信号
        self._interrupt = False
        # 同步锁
        self._lock = threading.Lock()
        # 播放线程常驻
        self._thread = threading.Thread(
            target=self._speak_worker,
            daemon=True
        )
        self._thread.start()

    def _speak_worker(self):
        stream = None
        while True:
            if self._current_text is None:
                time.sleep(0.2)
                continue
            with self._lock:
                text = self._current_text
                self._current_text = None
                self._interrupt = False
            try:
                for chunk in self.voice.synthesize(text):
                    if self._interrupt:
                        logger.info("打断播放")
                        break
                    if stream is None:
                        stream = sd.OutputStream(
                            samplerate=chunk.sample_rate,
                            channels=chunk.sample_channels,
                            dtype="int16",
                        )
                        stream.start()
                    audio = np.frombuffer(chunk.audio_int16_bytes, dtype=np.int16)
                    stream.write(audio)
                logger.info("播放结束")
            except Exception as e:
                logger.error(f"播放错误: {e}")
            finally:
                if stream:
                    try:
                        stream.stop()
                        stream.close()
                    except:
                        pass
                    stream = None

    def speak(self, text: str):
        with self._lock:
            self._interrupt = True
            self._current_text = text

    def stop(self):
        with self._lock:
            self._interrupt = True
