import queue
import threading

from langchain_core.messages import HumanMessage
from loguru import logger

import meow_ai_agent.constants.config as config
from meow_ai_agent.utils.audio_input import create_audio_processor
from meow_ai_agent.utils.output import OutputManager


class InputManager:
    """输入管理器 - 支持文本和语音输入"""

    def __init__(self, app_instance, thread_config: dict):
        self.app = app_instance
        self.thread_config = thread_config
        self.input_queue = queue.Queue(maxsize=5)
        self.stop_event = threading.Event()
        self.audio_processor = None
        self.output_manager = OutputManager(
            output_mode=config.output_mode,
            speak_model_path=config.speak_model_path
        )

    def on_audio_text(self, text: str):
        """音频识别回调"""
        if not text:
            return
        logger.info(f"语音识别: {text}")
        try:
            self.input_queue.put_nowait(text)
        except queue.Full:
            logger.warning(f"输入队列满，丢弃文本: {text}")

    def _init_audio(self):
        """初始化音频处理器"""
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

    def _consume_loop(self):
        """消费队列（主线程）"""
        while not self.stop_event.is_set():
            try:
                user_input = self.input_queue.get()
                if user_input is None:
                    break
                self._process_input(user_input)
            except Exception as e:
                logger.error(f"消费队列异常: {e}")

    def audio_input(self):
        logger.info("语音输入模式启动...")
        try:
            self._init_audio()
            logger.info("音频处理器初始化完成")
            self.audio_processor.start()
            logger.info("语音模式已启动")
            # 主线程消费
            self._consume_loop()
        except KeyboardInterrupt:
            logger.info("收到中断信号，准备退出...")
        except Exception as e:
            logger.error(f"音频模式异常: {e}")
            logger.warning("切换到文本模式...")
            self.text_input()
        finally:
            self.stop()

    def stop(self):
        self.stop_event.set()
        try:
            self.input_queue.put_nowait(None)
        except queue.Full:
            pass
        if self.audio_processor:
            self.audio_processor.stop()
        logger.info("音频处理已停止")


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

    def _process_input(self, user_input: str):
        """处理用户输入"""
        try:
            # for chunk in self.app.stream(
            #         {"messages": [HumanMessage(content=user_input)]},
            #         config=self.thread_config,
            #         stream_mode="messages"
            # ):
            #     msg_chunk, metadata = chunk
            #
            #     # 过滤空 token
            #     if not msg_chunk.content:
            #         continue
            #
            #     # 输出AI回复
            #     self.output_manager.output(msg_chunk.content)
            #
            # self.output_manager.output("\n")  # 换行

            # 非流式
            result = self.app.invoke(
                {"messages": [HumanMessage(content=user_input)]},
                config=self.thread_config
            )

            config.audio_is_playing = True
            self.output_manager.output(result["messages"][-1].content)

        except Exception as e:
            logger.error(f"处理输入时出错: {e}")

    def start(self):
        """根据配置启动相应的输入模式"""
        logger.info(f"启动输入模式: {config.input_mode}")

        if config.input_mode == "audio":
            self.audio_input()
        else:
            self.text_input()
