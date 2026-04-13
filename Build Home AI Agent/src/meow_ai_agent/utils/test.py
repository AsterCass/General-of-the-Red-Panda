# python -m pip install langchain langchain-core langchain-ollama langgraph redis loguru
import re
from typing import TypedDict, Annotated, Optional

from langchain.tools import tool
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langgraph.checkpoint.redis import RedisSaver
from langgraph.constants import END
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from loguru import logger

OLLAMA_BASE_URL = "http://localhost:11434"
REDIS_URL = "redis://localhost:6379"
MODEL_NAME = "qwen3:14b-q4_K_M"
LIGHT_MODEL_NAME = "qwen2.5:1.5b"


# ==================== 模型配置 ====================
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]  # 自动合并消息历史
    pending_action: Optional[AIMessage] | None  # 工具操作
    confirmed: Optional[bool] | None  # 工具确认


llm = ChatOllama(
    model=MODEL_NAME,
    base_url=OLLAMA_BASE_URL,
    tags=["nostream"],
)

llm_l = ChatOllama(
    model=LIGHT_MODEL_NAME,
    base_url=OLLAMA_BASE_URL,
    temperature=0,
    tags=["nostream"],
)

confirm_words = [
    "是", "好的", "确认", "ok", "yes", "sure", "嗯", "可以", "行", "行", "是的", "确定"
]

system_prompt_confirm = f"""
你是一个分类器，只能回答 YES 或 NO。

判断输入内容是否表示肯定含义，常见肯定含义词：

${confirm_words}

规则：
- 表示同意、确认、肯定、认同则输出 YES
- 表示拒绝、取消则输出 NO
- 不确定、无关则输出 NO

只输出 YES 或 NO
"""
prompt_confirm = ChatPromptTemplate.from_messages([("system", system_prompt_confirm), ("placeholder", "{messages}"), ])

system_prompt_tool = """
你是一个智能家居助手，必须严格遵守以下规则：
1. 工具调用必须通过系统提供的 function calling 机制完成。
2. 当需要执行设备或者工具操作时，必须使用 tool_call，不允许模拟 tool_call ，不允许在文本中输出 JSON。
3. 如果不能调用工具，就正常回答。
4. 不要自问自答。
5. 你的回复必须是纯文本，不允许包含“AI:”、“Assistant:”等角色前缀。
6. 直接调用工具即可，不要再次询问。
"""
prompt_tool = ChatPromptTemplate.from_messages([("system", system_prompt_tool), ("placeholder", "{messages}"), ])


# ==================== 工具配置 ====================

def smart_tool(**meta):
    def wrapper(func):
        t = tool(func)
        t.metadata = meta
        return t

    return wrapper


@smart_tool(need_confirm=True, category="device")
def turn_off_light_bedroom() -> str:
    """关闭卧室灯光"""
    logger.info("Turn off light 1...")
    return "卧室灯光已经关闭"


@smart_tool(need_confirm=True, category="device")
def turn_on_light_living_room() -> str:
    """打开客厅灯光"""
    logger.info("Turn on light 1...")
    return "客厅灯光已经打开"


@smart_tool(need_confirm=True, category="device")
def turn_off_light_living_room() -> str:
    """关闭客厅灯光"""
    logger.info("Turn off light 2...")
    return "客厅灯已经关闭"


@smart_tool(need_confirm=True, category="device")
def close_window_living_room() -> str:
    """关闭客厅窗户"""
    logger.info("Closing window...")
    return "客厅窗户已关闭"


@smart_tool(need_confirm=True, category="device")
def turn_on_heating_bedroom() -> str:
    """打开卧室暖气"""
    logger.info("Turn on heating...")
    return "卧室暖气已经打开"


@smart_tool(need_confirm=False, category="device")
def open_curtain_living_room() -> str:
    """打开客厅窗帘"""
    logger.info("Open curtain living room...")
    return "客厅窗帘已打开"


@smart_tool(need_confirm=False, category="device")
def close_curtain_living_room() -> str:
    """关闭客厅窗帘"""
    logger.info("Close curtain living room...")
    return "客厅窗帘已关闭"


tools = [turn_off_light_bedroom, turn_off_light_living_room, close_window_living_room, turn_on_light_living_room,
         turn_on_heating_bedroom, open_curtain_living_room, close_curtain_living_room]
tool_node = ToolNode(tools=tools)
tool_map = {t.name: t for t in tools}
llm_with_tools = llm.bind_tools(tools)


# ==================== 节点定义 ====================


def intent_tool_node(state: AgentState):
    messages = state["messages"]
    # 如果已经有待办，则不需要调用LLM，也就不用返回值更新状态
    if state.get("pending_action"):
        return {"confirmed": False}
    response = llm_with_tools.invoke(prompt_tool.format(messages=messages))
    # Tool 匹配
    if hasattr(response, "tool_calls") and response.tool_calls:
        this_tool = response.tool_calls[0]
        tool_name = this_tool["name"]
        to = tool_map.get(tool_name)
        need_confirm = to.metadata.get("need_confirm", True)
        if need_confirm:
            return {
                "pending_action": response,
                "messages": [
                    AIMessage(content=f"您确定要执行{to.description}操作吗？")
                ]
            }
        else:
            return {
                "pending_action": response,
                "confirmed": True,
            }
    # 这里可以防止AI自己自创一个方法然后幻觉执行
    # 但是也有问题，如果你问类似你能支持什么操作，他可能会把所有的支持打印出来，此时也会执行
    for te in tool_map:
        pattern = rf'["\']name["\']:\s*["\']{te}["\']'
        if re.search(pattern, response.content):
            logger.info(f"Illusion match")
            to = tool_map.get(te)
            need_confirm = to.metadata.get("need_confirm", True)
            fake_message = AIMessage(
                content="",
                tool_calls=[{
                    "name": te,
                    "args": {},
                    "type": "tool_call",
                    "id": "fallback",
                }]
            )
            if need_confirm:
                return {
                    "pending_action": fake_message,
                    "messages": [
                        AIMessage(content=f"您确定要执行{to.description}操作吗？")
                    ]
                }
            else:
                return {
                    "pending_action": fake_message,
                    "confirmed": True,
                }
    return {"messages": [response]}


def confirm_tool_node(state: AgentState):
    # 字符串判断
    text = state["messages"][-1].content.lower()
    if text in confirm_words:
        return {"confirmed": True}
    # LLM 保底
    result = llm_l.invoke(
        prompt_confirm.format_messages(
            messages=[HumanMessage(content=text)],
        )
    ).content.strip().upper()
    logger.info(f"confirm classify result: {result}")
    if "YES" in result:
        return {"confirmed": True}
    else:
        return {"pending_action": None, "confirmed": None}


def prepare_tool_node(state: AgentState):
    logger.info("Preparing tool node")
    return {
        "messages": [state["pending_action"]],
        "pending_action": None,
        "confirmed": None
    }


def route_after_intent_tool_node(state: AgentState):
    if (state.get("pending_action")) and (state.get("confirmed") is not None):
        if state["confirmed"]:
            return "prepare_tool_node"
        else:
            return "confirm_tool_node"
    return END


def route_after_confirm_tool_node(state: AgentState):
    if state.get("confirmed"):
        return "prepare_tool_node"
    return "intent_tool_node"


# ==================== 图 ====================


builder = StateGraph(AgentState)
builder.add_node("intent_tool_node", intent_tool_node)
builder.add_node("confirm_tool_node", confirm_tool_node)
builder.add_node("prepare_tool_node", prepare_tool_node)
builder.add_node("tool_node", tool_node)

builder.set_entry_point("intent_tool_node")

builder.add_conditional_edges(
    "intent_tool_node",
    route_after_intent_tool_node,
    {
        "confirm_tool_node": "confirm_tool_node",
        "prepare_tool_node": "prepare_tool_node",
        END: END,
    }
)

builder.add_conditional_edges(
    "confirm_tool_node",
    route_after_confirm_tool_node,
    {
        "intent_tool_node": "intent_tool_node",
        "prepare_tool_node": "prepare_tool_node",
    }
)

builder.add_edge("prepare_tool_node", "tool_node")
builder.add_edge("tool_node", END)


def main():
    """程序主入口"""
    with RedisSaver.from_conn_string(REDIS_URL) as memory:
        memory.setup()

        this_app = builder.compile(checkpointer=memory)
        thread_config = {"configurable": {"thread_id": "thread_010"}}
        print("语言模型已启动，输入 exit 退出。")
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


main()
