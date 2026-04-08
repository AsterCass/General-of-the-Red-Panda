from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langgraph.constants import END
from langgraph.graph import StateGraph
from loguru import logger

import meow_ai_agent.model.base as base
import meow_ai_agent.model.intent as intent
import meow_ai_agent.model.rag as rag
import meow_ai_agent.model.tools as tools
from meow_ai_agent.constants.enums import IntentStatus

# ==================== !!! 因为要接入多种功能,方便测试起见，这里简化语义路由，并且单次对话不再更换确定的路由 !!! ====================
# ==================== !!! 即：对首句话，使用 semantic router 或者 LLM 判断 !!! ====================
# ==================== !!! 比如判断是工具，则后续对话都只走工具相关 langgraph !!! ====================
# ==================== !!! 后续开发可以合并多个功能，方案1：需要每次都联系上下文进行意图判断，资源消耗比较大 !!! ====================
# ==================== !!! 方案2：单纯使用类似 semantic router 的话，单句话没有上下文，容易误判 !!! ====================
# ==================== !!! 或者方案3：最简单的方法就是依靠LLM提示词，但是效果不稳定 !!! ====================
# ==================== !!! 生产角度可以联合这三个方案，当前 AgentState 中 IntentStatus 可以保留 !!! ====================
# ==================== !!! 比如当前为工具，使用 semantic router 或 LLM 强置信为 RAG 时候切换 !!! ====================


# ==================== 模型配置 ====================

system_prompt_chat = """
你是一个带有感情的聊天对象，需要遵守以下规则：
0. 你叫由乃。
1. 你热情礼貌。
2. 你对不了解的事情都很好奇。
3. 你会认真倾听，并且帮助分析。
"""
prompt_chat = ChatPromptTemplate.from_messages([("system", system_prompt_chat), ("placeholder", "{messages}"), ])


# ==================== 节点定义 ====================

def not_support_node(state: base.AgentState):
    logger.info("Not support node")
    return {
        "messages": [
            AIMessage(content=f"当前操作暂不支持")
        ],
        "intent": None,
        "intent_force": None,
        "pending_action": None,
        "confirmed": None,
    }


def intent_chat_node(state):
    return (
        prompt_chat
        | base.llm
        | RunnableLambda(lambda msg: {
            "messages": [msg]
        })
    )

# ==================== 路由定义 ====================

def route_after_intent_single_node(state: base.AgentState):
    if state.get("intent") and state.get("intent") == IntentStatus.RAG.value:
        return "intent_rag_node"
    if state.get("intent") and state.get("intent") == IntentStatus.WEB.value:
        return "not_support_node"
    if state.get("intent") and state.get("intent") == IntentStatus.TOOL.value:
        return "intent_tool_node"
    return "intent_chat_node"


def route_after_intent_tool_node(state: base.AgentState):
    if (state.get("pending_action")) and (state.get("confirmed") is not None):
        if state["confirmed"]:
            return "prepare_tool_node"
        else:
            return "confirm_tool_node"
    return END


def route_after_confirm_tool_node(state: base.AgentState):
    if state.get("confirmed"):
        return "prepare_tool_node"
    return "intent_tool_node"


# ==================== 流转图绘制 ====================

# 节点
builder = StateGraph(base.AgentState)
builder.add_node("intent_single_node", intent.intent_single_node)
builder.add_node("not_support_node", not_support_node)
# 工具
builder.add_node("intent_tool_node", tools.intent_tool_node)
builder.add_node("confirm_tool_node", tools.confirm_tool_node)
builder.add_node("prepare_tool_node", tools.prepare_tool_node)
builder.add_node("tool_node", tools.tool_node)
# 聊天
builder.add_node("intent_chat_node", intent_chat_node)
# 检索
builder.add_node("intent_rag_node", rag.intent_rag_node)

# 连接
builder.set_entry_point("intent_single_node")
builder.add_conditional_edges(
    "intent_single_node",
    route_after_intent_single_node,
    {
        "not_support_node": "not_support_node",
        "intent_chat_node": "intent_chat_node",
        "intent_tool_node": "intent_tool_node",
        "intent_rag_node": "intent_rag_node",
    }
)
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
builder.add_edge("not_support_node", END)
builder.add_edge("intent_chat_node", END)
builder.add_edge("intent_rag_node", END)

# ==================== 编译 ====================

# memory = MemorySaver()
# app = builder.compile(checkpointer=memory)
