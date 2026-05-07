from collections import deque
from enum import Enum
from typing import TypedDict, Annotated

import redis
from flask import Flask, Response, request
from flask import jsonify
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_ollama import ChatOllama
from langgraph.checkpoint.redis import RedisSaver
from langgraph.constants import END
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages

redis_cli = redis.Redis(host='localhost', port=6379)


class MessageType(Enum):
    AI = ("ai", 0)
    HUMAN = ("human", 1)

    def __init__(self, label, code):
        self.label = label
        self.code = code

    def to_int(self):
        return self.code

    @classmethod
    def from_string(cls, value: str):
        value = value.lower().strip()
        for item in cls:
            if item.label == value:
                return item
        return cls.AI


def delete_session(session_id: str):
    pattern = f"*:{session_id}:__empty__*"

    cursor = 0
    keys_to_delete = []

    while True:
        cursor, keys = redis_cli.scan(cursor=cursor, match=pattern, count=100)
        keys_to_delete.extend(keys)

        if cursor == 0:
            break

    if keys_to_delete:
        redis_cli.delete(*keys_to_delete)

    return len(keys_to_delete)


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]  # 自动合并消息历史


system_prompt_chat = """
你是一个聊天机器人，需要遵守以下规则：
1. 亲切礼貌，不卑不亢。
2. 乐于给出建议。
"""

prompt_chat = ChatPromptTemplate.from_messages([("system", system_prompt_chat), ("placeholder", "{messages}"), ])

llm = ChatOllama(
    model="qwen2.5:1.5b",
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

# 正确方式：先创建 saver 对象
redis_saver = RedisSaver.from_conn_string("redis://localhost:6379")
with redis_saver as memory:
    memory.setup()
this_app = builder.compile(checkpointer=memory)

app = Flask(__name__)


@app.route('/health')
def health():
    return jsonify({"status": 200}), 200


@app.route('/online', methods=['GET'])
def online():
    return {"status": 200}


@app.route('/clear', methods=['POST'])
def clear_history():
    session_id = request.args.get('session_id')
    if not session_id:
        return {"status": 200, "data": True}
    try:
        delete_session(session_id)
        return {"status": 200, "data": True}
    except Exception as e:
        print(e)
        return {"status": 400, "data": False}


@app.route('/history', methods=['GET'])
def get_history():
    session_id = request.args.get('session_id')
    if not session_id:
        return {"error": "missing session_id"}, 400

    thread_config = {"configurable": {"thread_id": session_id}}
    try:
        state = this_app.get_state(thread_config)
        if not state or not state.values or "messages" not in state.values:
            return {"status": 200, "data": []}

        history = deque([])
        for msg in state.values["messages"]:
            history.appendleft({
                "type": MessageType.from_string(msg.type).to_int(),
                "content": msg.content
            })
        return {"status": 200, "data": list(history)}
    except Exception as e:
        print(e)
        return {"status": 400, "data": []}


@app.route('/stream', methods=['GET'])
def ai_stream():
    user_input = request.args.get('user_input')
    session_id = request.args.get('session_id')

    def generate():
        thread_config = {"configurable": {"thread_id": session_id}}
        message = HumanMessage(content=user_input)

        try:
            for chunk in this_app.stream(
                    {"messages": [message]},
                    config=thread_config,
                    stream_mode="messages"
            ):
                msg_chunk, metadata = chunk
                if not msg_chunk.content:
                    continue

                yield f"data: {msg_chunk.content}\n"

            yield "data: [[DONE]]\n"

        except Exception as e:
            yield f"data: [[ERROR]] {str(e)}\n"

    return Response(generate(), content_type='text/event-stream')


if __name__ == '__main__':
    app.run()
