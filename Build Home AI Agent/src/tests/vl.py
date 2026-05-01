import base64
import os
from typing import TypedDict, Annotated, List

from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_ollama import ChatOllama
from langgraph.checkpoint.redis import RedisSaver
from langgraph.constants import END
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages


# ====================== 辅助函数：图片转 base64 ======================
def encode_image_to_base64(image_path: str) -> str:
    """将本地图片转为 base64 字符串"""
    abs_path = os.path.abspath(image_path)
    if not os.path.exists(abs_path):
        raise FileNotFoundError(f"图片不存在: {abs_path}")

    with open(abs_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded

image_paths = [
    "data/x1.jpg",
    "data/x2.jpg",
    "data/x3.jpg",
]

image_base64_list: List[str] = []
for path in image_paths:
    try:
        b64 = encode_image_to_base64(path)
        image_base64_list.append(b64)
        print(f"✓ 已加载图片: {path}")
    except Exception as e:
        print(f"✗ 加载失败 {path}: {e}")


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]  # 自动合并消息历史


system_prompt_chat = """
你是一个专门处理图片的机器人，用户会给你发送多张图片，你需要根据所有图片内容进行分析和回答。
请记住这些是预加载的图片，用户会针对它们提问。
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
        else:
            if not image_paths:
                print("默认图片集合不能为空")
                break

            content = [{"type": "text", "text": user_input}]
            for b64 in image_base64_list:
                content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{b64}"  # 或 image/png，根据实际格式调整
                    }
                })
            message = HumanMessage(content=content)

            for chunk in this_app.stream(
                    {"messages": [message]},
                    config=thread_config,
                    stream_mode="messages"
            ):
                msg_chunk, metadata = chunk

                # 过滤空 token
                if not msg_chunk.content:
                    continue

                print(msg_chunk.content, end="", flush=True)

            print()
