import threading
import time
from pathlib import Path
from queue import Queue, Full

from faster_qwen3_tts import FasterQwen3TTS
from loguru import logger

from meow_ai_agent.utils.stream_play import StreamPlayer


class AudioOutput:
    """
    # https://github.com/andimarafioti/faster-qwen3-tts/issues/43
    # https://github.com/andimarafioti/faster-qwen3-tts/issues/96
    # https://github.com/HaujetZhao/Qwen3-TTS-GGUF
    # https://modelscope.cn/collections/Qwen/Qwen3-TTS
    """

    def __init__(self, model_path: str):
        if not Path(model_path).is_dir():
            raise FileNotFoundError(f"模型文件不存在: {model_path}")

        self.model = FasterQwen3TTS.from_pretrained(model_path)
        self.thisPlay = StreamPlayer(on_finished=lambda: logger.info("输出音频播放完成"))
        logger.info(f"模型加载成功：{model_path}")

        # 当前要播放的文本
        self.text_queue = Queue(maxsize=10)
        # 同步锁
        self._lock = threading.Lock()
        # 播放线程常驻
        self._thread = threading.Thread(
            target=self._speak_worker,
            daemon=True
        )
        self._thread.start()

    def _speak_worker(self):
        while True:
            with self._lock:
                if self.text_queue.empty():
                    time.sleep(0.1)
                    continue
                current_text = self.text_queue.get()
                try:
                    for audio_chunk, sr, timing in self.model.generate_custom_voice_streaming(
                            text=current_text,
                            language="Chinese",
                            speaker="Serena",
                            non_streaming_mode=False,
                    ):
                        self.thisPlay(audio_chunk, sr)
                    self.thisPlay.end_segment()
                except Exception as e:
                    logger.error(f"播放异常: {e}")

    def speak(self, text: str):
        logger.info(f"进入输出队列文本: {text}")
        with self._lock:
            try:
                self.text_queue.put(text, block=False)
            except Full:
                logger.warning("音频输出堆栈满")
            except Exception as e:
                logger.error(f"音频输出堆栈异常: {e}")
