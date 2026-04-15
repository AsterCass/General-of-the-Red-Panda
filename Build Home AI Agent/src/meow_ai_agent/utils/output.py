import threading
import time
from pathlib import Path

from faster_qwen3_tts import FasterQwen3TTS
from loguru import logger

from meow_ai_agent.utils.stream_play import StreamPlayer


class Reader:
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
        logger.info(f"模型加载成功：{model_path}")

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
        while True:
            if self._current_text is None:
                time.sleep(0.2)
                continue
            logger.info(f"Start play {self._current_text}")
            thisPlay = StreamPlayer()
            try:
                for audio_chunk, sr, timing in self.model.generate_custom_voice_streaming(
                        text=self._current_text,
                        language="Chinese",
                        speaker="Serena",
                        non_streaming_mode=False,
                ):
                    thisPlay(audio_chunk, sr)
            finally:
                self._current_text = None
                thisPlay.close()

    def speak(self, text: str):
        with self._lock:
            self._interrupt = True
            self._current_text = text

    def stop(self):
        with self._lock:
            self._interrupt = True


class OutputManager:
    """输出管理器 - 支持文本和语音输出"""

    def __init__(self, output_mode: str, speak_model_path: str = None):
        self.output_mode = output_mode
        self.reader = None
        if output_mode == "audio" and speak_model_path:
            try:
                self.reader = Reader(speak_model_path)
            except Exception as e:
                logger.error(f"语音模型加载失败: {e}")
                logger.warning("切换到文本输出模式")
                self.output_mode = "text"

    def output(self, text: str):
        """输出文本"""
        # 过滤掉内部数据输出，如工具调用信息和确认结果
        logger.info(f"Output: {text}")
        if ('tool_call' in text or
                text.strip().startswith('[') or
            text.strip().upper() in ['YES', 'NO']):
            return
        if self.output_mode == "audio" and self.reader:
            self.reader.speak(text)
        else:
            print(text, end="", flush=True)

    def stop(self):
        """停止输出"""
        if self.reader:
            self.reader.stop()
