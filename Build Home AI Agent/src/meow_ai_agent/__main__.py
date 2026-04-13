from langgraph.checkpoint.redis import RedisSaver

import meow_ai_agent.constants.config as config
import meow_ai_agent.constants.env as env
import meow_ai_agent.model.app as app
from meow_ai_agent.config.logging import setup_logging
from meow_ai_agent.constants.config import service_settings
from meow_ai_agent.utils.input import InputManager


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

        # 创建输入管理器并启动
        input_manager = InputManager(this_app, thread_config)
        input_manager.start()


if __name__ == "__main__":
    main()
