from langchain_core.messages import HumanMessage

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

    thread_config = {"configurable": {"thread_id": "home_assistant_001"}}
    print("由乃智能家居助手已启动（LangGraph 版），输入 exit 退出。")
    while True:
        user_input = input(">>> ")
        if user_input == "exit":
            break

        result = app.app.invoke(
            {"messages": [HumanMessage(content=user_input)]},
            config=thread_config
        )

        print(result["messages"][-1].content)


if __name__ == "__main__":
    main()
