import time
from typing import TypedDict, Annotated

from flask import Flask, Response, request
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_ollama import ChatOllama
from langgraph.checkpoint.redis import RedisSaver
from langgraph.constants import END
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
import redis

redis_cli = redis.Redis(host='localhost', port=6379)


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
1. 使用自然口语表达，而不是书面表达。
2. 禁止使用任何 Markdown 格式（如 **、*、#、- 等）。
3. 不要使用列表、标题、加粗、代码块等格式。
4. 不要使用括号补充说明或解释性文字
5. 可以适当加入语气词，让表达更自然。
6. 你的回答必须可以被直接朗读出来，不要包含任何不适合朗读的内容。
"""

prompt_chat = ChatPromptTemplate.from_messages([("system", system_prompt_chat), ("placeholder", "{messages}"), ])

llm = ChatOllama(
    model="qwen3:14b-q4_K_M",
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

# server
app = Flask(__name__)

@app.route('/online', methods=['GET'])
def online():
    return {"status": 200}

@app.route('/clear', methods=['POST'])
def clear_history():
    session_id = request.args.get('session_id')
    if not session_id:
        return {"error": "missing session_id"}, 400

    try:
        # 直接删redis
        delete_session(session_id)

        return {"status": 200}

    except Exception as e:
        return {"error": str(e)}, 500


@app.route('/history', methods=['GET'])
def get_history():
    session_id = request.args.get('session_id')
    if not session_id:
        return {"error": "missing session_id"}, 400

    thread_config = {"configurable": {"thread_id": session_id}}
    try:
        state = this_app.get_state(thread_config)
        print(state)
        if not state or not state.values or "messages" not in state.values:
            return {"messages": []}

        history = []
        for msg in state.values["messages"]:
            history.append({
                "type": msg.type,
                "content": msg.content
            })
        return {"messages": history}
    except Exception as e:
        return {"error": str(e)}, 500

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

                yield f"data: {msg_chunk.content}\n\n"
                time.sleep(0.3)

            yield "data: [[DONE]]\n\n"

        except Exception as e:
            yield f"data: [[ERROR]] {str(e)}\n\n"

    return Response(generate(), content_type='text/event-stream')


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
