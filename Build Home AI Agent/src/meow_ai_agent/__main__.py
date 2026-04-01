from langchain_classic.agents import create_openai_tools_agent, AgentExecutor
from langchain_classic.memory import ConversationBufferMemory
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama

import meow_ai_agent.constants.config as config
from meow_ai_agent.config.logging import setup_logging
from meow_ai_agent.constants.env import print_env
from meow_ai_agent.utils.light import close_window, turn_on_heating, turn_off_light_2, turn_off_light_1

OLLAMA_BASE_URL = "http://localhost:11434"
MODEL_NAME = "qwen2.5:7b"
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
COLLECTION_NAME = "docs"

search_wrapper = DuckDuckGoSearchAPIWrapper(
    # backend="bing",        # 推荐先试 bing（对中文和时效性内容通常更稳）
    # backend="html",      # 纯 DuckDuckGo html 页面
    backend="html",  # 轻量版，速度快但结果可能少
    region="cn-zh",  # 全球（推荐）
    safesearch="moderate",
)


def main():
    """程序主入口"""
    # 基础配置
    setup_logging(False)
    print_env()
    config.load_config()
    # LLM
    llm = ChatOllama(
        model=MODEL_NAME,
        base_url=OLLAMA_BASE_URL,
    )
    # 工具
    tools = [turn_off_light_1, turn_off_light_2, close_window, turn_on_heating]
    # Prompt
    system_prompt = """
你是一个智能家居助手，必须严格遵守以下规则：
0. 你叫由乃
1. 所有设备控制操作都是高危操作。
2. 绝对不要直接调用任何设备控制工具。
3. 当用户要求控制设备时，你只能做一件事：用自然语言询问用户是否确认，例如：您确定要关闭卧室的灯吗？
4. 只有当用户在本轮对话中明确回复同意词时，你才可以在下一轮调用对应的工具。
5. 每次回复只做一件事：要么询问确认，要么执行工具后总结，不要同时做两件事。
"""

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )

    # Agent
    agent = create_openai_tools_agent(llm, tools, prompt)
    executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        memory=memory
    )
    while True:
        user_input = input(">>> ")
        if user_input == "exit":
            break

        result = executor.invoke({"input": user_input})
        print(result["output"])


if __name__ == "__main__":
    main()
