import queue

from langchain_core.messages import HumanMessage
from loguru import logger

import meow_ai_agent.constants.config as config
from meow_ai_agent.utils.audio_input import create_audio_processor
from meow_ai_agent.utils.output import clean_output


class InputManager:
    """输入管理器 - 支持文本和语音输入"""

    def __init__(self, app_instance, thread_config: dict):
        self.app = app_instance
        self.thread_config = thread_config
        self.input_queue = queue.Queue()
        self.audio_processor = None

    def on_audio_text(self, text: str):
        """音频识别回调"""
        if text:
            logger.info(f"语音识别: {text}")
            self.input_queue.put(text)

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

                self._process_input(user_input)
            except KeyboardInterrupt:
                logger.info("收到中断信号")
                break
            except Exception as e:
                logger.error(f"输入处理错误: {e}")

    def audio_input(self):
        """语音输入模式"""
        try:
            logger.info("由乃智能家居助手已启动（语音输入模式），准备初始化音频处理...")

            # 创建音频处理器
            self.audio_processor = create_audio_processor(
                model=config.audio_settings.model,
                vad=config.audio_settings.vad,
                language=config.audio_settings.language,
                sample_rate=config.audio_settings.sample_rate,
                chunk_duration=config.audio_settings.chunk_duration,
                min_silence_ms=config.audio_settings.min_silence_ms,
                min_audio_ms=config.audio_settings.min_audio_ms,
                vad_window_sec=config.audio_settings.vad_window_sec,
                on_text_callback=self.on_audio_text
            )

            logger.info("音频处理器初始化完成，开始监听...")
            print("音频输入模式已启动，按 Ctrl+C 停止监听...\n")

            # 启动音频处理
            self.audio_processor.start()

            # 主处理循环
            while True:
                try:
                    # 从队列获取识别的文本（超时10秒）
                    user_input = self.input_queue.get(timeout=10)
                    self._process_input(user_input)
                except queue.Empty:
                    # 继续等待输入
                    continue
                except KeyboardInterrupt:
                    logger.info("收到中断信号")
                    break

        except Exception as e:
            logger.error(f"音频输入初始化失败: {e}")
            logger.warning("切换到文本输入模式...")
            self.text_input()

        finally:
            if self.audio_processor:
                self.audio_processor.stop()
                logger.info("音频处理已停止")

    def _process_input(self, user_input: str):
        """处理用户输入"""
        try:
            for chunk in self.app.stream(
                    {"messages": [HumanMessage(content=user_input)]},
                    config=self.thread_config,
                    stream_mode="messages"
            ):
                msg_chunk, metadata = chunk

                # 过滤空 token
                if not msg_chunk.content:
                    continue

                # 输出AI回复
                print(clean_output(msg_chunk.content), end="", flush=True)

            print()  # 换行

        except Exception as e:
            logger.error(f"处理输入时出错: {e}")

    def start(self):
        """根据配置启动相应的输入模式"""
        logger.info(f"启动输入模式: {config.input_mode}")

        if config.input_mode == "audio":
            self.audio_input()
        else:
            self.text_input()
