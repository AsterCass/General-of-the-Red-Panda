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
        # 这里不仅会存对话，也会存最后的 AgentState
        thread_config = {"configurable": {"thread_id": "home_assistant_005"}}
        print("由乃智能家居助手已启动（LangGraph 版），输入 exit 退出。")
        while True:
            user_input = input(">>> ")
            if user_input == "exit":
                break

            for chunk in this_app.stream(
                    {"messages": [HumanMessage(content=user_input)]},
                    config=thread_config,
                    stream_mode="messages"
            ):
                msg_chunk, metadata = chunk

                # 过滤空 token
                if not msg_chunk.content:
                    continue

                # todo 合并放入消息队列，异步写入数据库
                print(msg_chunk.content, end="", flush=True)

            print()


if __name__ == "__main__":
    main()
