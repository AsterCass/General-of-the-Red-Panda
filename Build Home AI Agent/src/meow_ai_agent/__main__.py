import re
from typing import TypedDict, Annotated, Optional

from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_ollama import OllamaEmbeddings
from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import END
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from loguru import logger

import meow_ai_agent.constants.config as config
from meow_ai_agent.config.logging import setup_logging
from meow_ai_agent.constants.env import print_env
from meow_ai_agent.utils.light import turn_off_light_bedroom, turn_off_light_living_room, close_window_living_room, \
    turn_on_heating_bedroom, open_curtain_living_room, close_curtain_living_room

OLLAMA_BASE_URL = "http://localhost:11434"
MODEL_NAME = "qwen2.5:7b"
MODEL_NAME_LIGHT = "qwen2.5:0.5b"
EMBED_TEXT_MODEL_NAME = "nomic-embed-text"
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
COLLECTION_NAME = "docs"

search_wrapper = DuckDuckGoSearchAPIWrapper(
    backend="html",  # 轻量版，速度快但结果可能少
    region="cn-zh",  # 全球（推荐）
    safesearch="moderate",
)


# ====================== 状态 ======================
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]  # 自动合并消息历史
    pending_action: Optional[AIMessage] | None
    confirmed: Optional[bool] | None


# ====================== 模型 ======================
llm = ChatOllama(
    model=MODEL_NAME,
    base_url=OLLAMA_BASE_URL,
)

emb = OllamaEmbeddings(
    model=EMBED_TEXT_MODEL_NAME,
    base_url=OLLAMA_BASE_URL
)

llml = ChatOllama(
    model=MODEL_NAME_LIGHT,
    base_url=OLLAMA_BASE_URL,
    temperature=0
)

# ====================== 语义 ======================


system_prompt_l = """
你是一个分类器，只能回答 YES 或 NO。

判断输入内容是否表示肯定含义

常见肯定含义词：
- 好的
- 好的呢
- 好呀
- 可以
- 行
- 嗯
- 嗯嗯
- ok
- yes

规则：
- 表示同意、确认、肯定、认同 → YES
- 表示拒绝、取消 → NO
- 不确定、无关 → NO

只输出 YES 或 NO：
"""
prompt_l = ChatPromptTemplate.from_messages([("system", system_prompt_l), ("placeholder", "{messages}"), ])

# ====================== 工具 ======================

tools = [turn_off_light_bedroom, turn_off_light_living_room, close_window_living_room,
         turn_on_heating_bedroom, open_curtain_living_room, close_curtain_living_room]
tool_node = ToolNode(tools=tools)
tool_map = {t.name: t for t in tools}
llm_with_tools = llm.bind_tools(tools)

system_prompt = """
你是一个智能家居助手，必须严格遵守以下规则：
0. 你叫由乃。
1. 工具调用必须通过系统提供的 function calling 机制完成。
2. 当需要执行设备或者工具操作时，必须使用 tool_call，不允许模拟 tool_call ，不允许在文本中输出 JSON
3. 如果不能调用工具，就正常回答.
4. 不要自问自答。
"""
prompt = ChatPromptTemplate.from_messages([("system", system_prompt), ("placeholder", "{messages}"), ])


# 节点定义
def agent_node(state: AgentState):
    messages = state["messages"]
    logger.info(f"messages: {messages}")
    logger.info(state.get("pending_action"))
    # 如果已经有待办，则不需要调用LLM，也就不用返回值更新状态
    if state.get("pending_action"):
        return {"confirmed": False}
    response = llm_with_tools.invoke(prompt.format(messages=messages))
    # Tool 匹配
    if hasattr(response, "tool_calls") and response.tool_calls:
        logger.info(f"tool_calls: {response.tool_calls}")
        this_tool = response.tool_calls[0]
        tool_name = this_tool["name"]
        logger.info(f"tool_name: {tool_name}")
        tool = tool_map.get(tool_name)
        need_confirm = tool.metadata.get("need_confirm", True)
        if need_confirm:
            return {
                "pending_action": response,
                "messages": [
                    AIMessage(content=f"您确定要执行{tool.description}操作吗？")
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
            tool = tool_map.get(te)
            need_confirm = tool.metadata.get("need_confirm", True)
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
                        AIMessage(content=f"您确定要执行{tool.description}操作吗？")
                    ]
                }
            else:
                return {
                    "pending_action": fake_message,
                    "confirmed": True,
                }
    return {"messages": [response]}


# todo 优化方向：1. 制作了一个 Intent 分类专门判断用户意图，比如确认、拒绝、新指令、聊天等等
#  BGE 建 embedding 类似方式实现，放在 《手动指定》和 《小模型兜底》之间
# 2. 找找这个意图判断是否有比较好的专门的模型，或者自己训练（成本较大）
def confirm_node(state: AgentState):
    # 手动指定
    logger.info("To confirm a node")
    text = state["messages"][-1].content.lower()
    confirm_words = ["是", "好的", "确认", "ok", "yes", "sure", "嗯", "可以", "行", "行", "是的", "确定"]
    if text in confirm_words:
        return {"confirmed": True}
    # 小模型兜底
    result = llml.invoke(
        prompt_l.format_messages(
            messages=[HumanMessage(content=text)]
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


def route_after_agent(state: AgentState):
    logger.info("Route after agent")
    if (state.get("pending_action")) and (state.get("confirmed") is not None):
        if state["confirmed"]:
            return "prepare_action"
        else:
            return "confirm"
    return END


def route_after_confirm(state: AgentState):
    if state.get("confirmed"):
        return "prepare_action"
    return "agent"


# 节点
builder = StateGraph(AgentState)
builder.add_node("agent", agent_node)
builder.add_node("confirm", confirm_node)
builder.add_node("prepare_action", prepare_tool_node)
builder.add_node("action", tool_node)

# 图
builder.set_entry_point("agent")
builder.add_conditional_edges(
    "agent",
    route_after_agent,
    {
        "confirm": "confirm",
        "prepare_action": "prepare_action",
        END: END,
    }
)
builder.add_conditional_edges(
    "confirm",
    route_after_confirm,
    {
        "agent": "agent",
        "prepare_action": "prepare_action",
    }
)
builder.add_edge("prepare_action", "action")
builder.add_edge("action", END)

# 编译
memory = MemorySaver()
app = builder.compile(checkpointer=memory)


def main():
    """程序主入口"""
    # 基础配置
    setup_logging(False)
    print_env()
    config.load_config()

    thread_config = {"configurable": {"thread_id": "home_assistant_001"}}
    print("由乃智能家居助手已启动（LangGraph 版），输入 exit 退出。")
    while True:
        user_input = input(">>> ")
        if user_input == "exit":
            break

        result = app.invoke(
            {"messages": [HumanMessage(content=user_input)]},
            config=thread_config
        )

        print(result["messages"][-1].content)


if __name__ == "__main__":
    main()
