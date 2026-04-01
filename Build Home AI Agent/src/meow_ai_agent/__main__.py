from langchain_classic.agents import create_openai_tools_agent, AgentExecutor
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_core.prompts import ChatPromptTemplate
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
        temperature=0.3,
        base_url=OLLAMA_BASE_URL
    )
    # 工具
    tools = [turn_off_light_1, turn_off_light_2, close_window, turn_on_heating,
             DuckDuckGoSearchRun(name="web_search", api_wrapper=search_wrapper), ]
    # Prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", """你是一个智能助手：
    规则：
    1. 涉及设备控制（灯）→ 使用工具
    2. 不知道答案才使用联网搜索，并标注是联网的结果
    """),
        ("user", "{input}"),
        ("placeholder", "{agent_scratchpad}")
    ])
    # Agent
    agent = create_openai_tools_agent(llm, tools, prompt)
    executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True
    )
    while True:
        user_input = input(">>> ")
        if user_input == "exit":
            break

        result = executor.invoke({"input": user_input})
        print(result["output"])


if __name__ == "__main__":
    main()
