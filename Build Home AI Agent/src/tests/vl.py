from typing import TypedDict, Annotated

from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_ollama import ChatOllama
from langgraph.checkpoint.redis import RedisSaver
from langgraph.constants import END
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages

image_paths = [
    "data/x1.jpg",
    "data/x2.jpg",
    "data/x3.jpg",
]


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]  # 自动合并消息历史


system_prompt_chat = """
你是一个专门处理图片的机器人，用户会给你发送图片，你需要根据图片内容进行分析和回答。
"""
prompt_chat = ChatPromptTemplate.from_messages([("system", system_prompt_chat), ("placeholder", "{messages}"), ])

llm = ChatOllama(
    model="qwen3-vl:8b",
    base_url="http://localhost:11434",
)


def intent_chat_node(state):
    return (
            prompt_chat
            | llm
            | RunnableLambda(lambda msg: {
        "messages": [msg]
    })
    )


builder = StateGraph(AgentState)
builder.set_entry_point("intent_chat_node")
builder.add_node("intent_chat_node", intent_chat_node)
builder.add_edge("intent_chat_node", END)

with RedisSaver.from_conn_string("redis://localhost:6379") as memory:
    memory.setup()  # 只有首次需要

    this_app = builder.compile(checkpointer=memory)
    thread_config = {"configurable": {"thread_id": "home_assistant_001"}}
    print("输入 exit 退出。")
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

            print(msg_chunk.content, end="", flush=True)

        print()
