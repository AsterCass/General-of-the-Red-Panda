from loguru import logger

import meow_ai_agent.constants.config as config
from meow_ai_agent.audio.output import AudioOutput
from typing import Callable, Optional

class OutputManager:
    """输出管理器 - 支持文本和语音输出"""

    def __init__(self, before_output: Optional[Callable[[], None]] = None,
                 after_output: Optional[Callable[[], None]] = None):
        self.output_mode = config.output_mode
        self.speak_model_path = config.speak_model_path
        self.audio_output = None
        self.before_output = before_output
        self.after_output = after_output
        if self.output_mode == "audio" and self.speak_model_path:
            try:
                self.audio_output = AudioOutput(self.speak_model_path, self.after_output)
            except Exception as e:
                logger.error(f"输出音频模式异常: {e}")
                logger.warning("切换到文本输出模式")
                self.output_mode = "text"

    def output(self, text: str):
        """输出文本"""
        if self.before_output:
            self.before_output()
        # 过滤掉内部数据输出，如工具调用信息和确认结果
        if self.output_mode == "audio" and self.audio_output:
            self.audio_output.speak(text)
        else:
            print(text, end="", flush=True)
            if self.after_output:
                self.after_output()
