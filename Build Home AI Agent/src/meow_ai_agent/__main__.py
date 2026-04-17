from langchain_core.messages import HumanMessage
from langgraph.checkpoint.redis import RedisSaver
from loguru import logger

import meow_ai_agent.constants.config as config
import meow_ai_agent.constants.env as env
import meow_ai_agent.model.app as app
from meow_ai_agent.config.logging import setup_logging
from meow_ai_agent.constants.config import service_settings
from meow_ai_agent.utils.input_manager import InputManager
from meow_ai_agent.utils.output_manager import OutputManager


def main():
    """程序主入口"""
    # 基础配置
    setup_logging(False)
    env.print_env()
    config.load_config()

    # 初始化Redis内存
    with RedisSaver.from_conn_string(service_settings.redis_url) as memory:
        memory.setup()  # 只有首次需要

        # 编译应用
        this_app = app.builder.compile(checkpointer=memory)

        # 线程配置
        thread_config = {"configurable": {"thread_id": "home_assistant_007"}}

        # 输入管理器
        input_manager = InputManager()

        # 输出管理器
        # todo 这里在输出管理器中将暂停和恢复输入监听的函数传入，作为输出的前置和后置处理，是临时逻辑，后续使用声纹或者回声消除等方式处理
        output_manager = OutputManager(input_manager.pause_audio_input, input_manager.resume_audio_input)

        # 回调
        def process_input_callback(user_input: str):
            """处理用户输入"""
            logger.info(f"检测到输入内容：{user_input}")
            try:
                # 流式
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
                result = this_app.invoke(
                    {"messages": [HumanMessage(content=user_input)]},
                    config=thread_config
                )
                output_manager.output(result["messages"][-1].content + "\n")
            except Exception as e:
                logger.error(f"处理输入时出错: {e}")

        input_manager.set_callback(process_input_callback)

        # 输入管理器启动
        input_manager.start()


if __name__ == "__main__":
    main()
