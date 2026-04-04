from langchain_core.messages import HumanMessage
from langgraph.checkpoint.redis import RedisSaver

import meow_ai_agent.constants.config as config
import meow_ai_agent.constants.env as env
import meow_ai_agent.model.app as app
from meow_ai_agent.config.logging import setup_logging


def main():
    """程序主入口"""
    # 基础配置
    setup_logging(False)
    env.print_env()
    config.load_config()

    with RedisSaver.from_conn_string(env.REDIS_URL) as memory:
        memory.setup()  # 只有首次需要

        this_app = app.builder.compile(checkpointer=memory)
        thread_config = {"configurable": {"thread_id": "home_assistant_001"}}
        print("由乃智能家居助手已启动（LangGraph 版），输入 exit 退出。")
        while True:
            user_input = input(">>> ")
            if user_input == "exit":
                break

            # todo 改成流式输出，整个图的处理都要改
            result = this_app.invoke(
                {"messages": [HumanMessage(content=user_input)]},
                config=thread_config
            )

            # todo 放入消息队列，写入数据库
            print(result["messages"][-1].content)


if __name__ == "__main__":
    main()
