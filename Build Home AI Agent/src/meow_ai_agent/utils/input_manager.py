from typing import Callable

from loguru import logger

import meow_ai_agent.constants.config as config
from meow_ai_agent.audio.input import AudioInput


class InputManager:
    """输入管理器 - 支持文本和语音输入"""

    def __init__(self, callback: Callable[[str], None]):
        self.callback = callback

    def audio_input(self):
        logger.info("由乃智能家居助手已启动（语音输入模式）")
        try:
            audio_input = AudioInput(self.callback)
            audio_input.start()
        except KeyboardInterrupt:
            return
        except Exception as e:
            logger.error(f"输入音频模式异常: {e}")
            logger.warning("切换到文本输入模式...")
            self.text_input()


    def text_input(self):
        """文本输入模式"""
        logger.info("由乃智能家居助手已启动（文本输入模式），输入 exit 退出。")
        while True:
            try:
                user_input = input(">>> ")
                if user_input.lower() == "exit":
                    break
                if not user_input.strip():
                    continue
                self.callback(user_input)
            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.error(f"输入处理错误: {e}")

    def start(self):
        """根据配置启动相应的输入模式"""
        logger.info(f"启动输入模式: {config.input_mode}")
        if config.input_mode == "audio":
            self.audio_input()
        else:
            self.text_input()
