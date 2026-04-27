import threading
from pathlib import Path
from queue import Queue, Full
from typing import Callable, Optional

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

    def __init__(self, model_path: str, is_clone: bool, clone_audio: str, clone_audio_text: str,
                 after_output: Optional[Callable[[], None]] = None):
        if not Path(model_path).is_dir():
            raise FileNotFoundError(f"模型文件不存在: {model_path}")

        self.is_clone = is_clone
        self.clone_audio = clone_audio
        self.clone_audio_text = clone_audio_text
        self.model = FasterQwen3TTS.from_pretrained(model_path)
        self.thisPlay = StreamPlayer(on_finished=after_output)
        logger.info(f"模型加载成功：{model_path}")

        # 当前要播放的文本
        self.text_queue = Queue(maxsize=10)
        # 播放线程常驻
        self._thread = threading.Thread(
            target=self._speak_worker,
            daemon=True
        )
        self._thread.start()

    def _speak_worker(self):
        while True:
            current_text = self.text_queue.get()
            try:
                if self.is_clone:
                    for audio_chunk, sr, timing in self.model.generate_voice_clone_streaming(
                            text=current_text,
                            language="Chinese",
                            ref_audio=self.clone_audio,
                            ref_text=self.clone_audio_text,
                            non_streaming_mode=False,
                    ):
                        self.thisPlay(audio_chunk, sr)
                else:
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
        try:
            self.text_queue.put(text, block=False)
        except Full:
            logger.warning("音频输出堆栈满")
