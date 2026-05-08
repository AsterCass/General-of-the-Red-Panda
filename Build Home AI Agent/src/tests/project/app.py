from typing import TypedDict, Annotated, List, Optional

from langchain_core.messages import AIMessage
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langgraph.constants import END
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages

llm_text = ChatOllama(model="qwen3:14b-q4_K_M", base_url="http://localhost:11434", temperature=0.3)
llm_vl = ChatOllama(model="qwen3-vl:8b", base_url="http://localhost:11434", temperature=0.2)


class ProjectItem(TypedDict):
    name: Optional[str]
    url: Optional[str]
    price: Optional[float]
    desc: Optional[str]
    reason: Optional[str]


class Project(TypedDict):
    background: Optional[ProjectItem]
    avatar: Optional[ProjectItem]
    products: List[ProjectItem]
    script: Optional[str]
    max_price: Optional[int]
    style: Optional[str]


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    intent: Optional[str]
    project: Optional[Project]
    avatar_list: Optional[List[ProjectItem]]
    product_list: Optional[List[ProjectItem]]
    bg_list: Optional[List[ProjectItem]]
    is_confirm: Optional[bool]


system_prompt_intent = """
你是一个意图分类器。判断用户输入属于哪种类型，只允许输出以下三个单词之一（严格匹配，不要任何解释）：
NEW
MODIFY
CHAT
类型说明：
- NEW: 用户要创建新的推广内容项目（包含目标人群、风格、预算等信息）
- MODIFY: 用户对已有项目提出修改意见（仅在已有项目时适用）
- CHAT: 普通对话、问题咨询，或者其他无法判断的类型
"""
prompt_intent = ChatPromptTemplate.from_messages([("system", system_prompt_intent), ("placeholder", "{messages}"), ])


# ==================== 额外方法 ====================

def llm_classify(context: str):
    # 内部小模型，不流式
    ret = llm_text.invoke(
        prompt_intent.format_messages(
            messages=[HumanMessage(content=context)]
        )
    ).content.strip().upper()
    return ret


# ==================== 节点定义 ====================

def intent_node(state: AgentState):
    print("intent_node ... ")
    last_msg = state["messages"][-1].content
    has_project = state.get("project") is not None
    context = f"已有项目：{'是' if has_project else '否'}\n用户输入：{last_msg}"
    return {"intent": llm_classify(context)}


def new_project_node(state: AgentState):
    print("new_project_node ... ")
    return {
        "messages": [
            AIMessage(content="创建成功")
        ]
    }


def modify_project_node(state: AgentState):
    print("modify_project_node ... ")
    return {
        "messages": [
            AIMessage(content="修改成功")
        ]
    }


def chat_node(state: AgentState):
    print("chat_node ... ")
    return {
        "messages": [
            AIMessage(content="不聊天，谢谢")
        ]
    }


# ==================== 路由定义 ====================

def route_after_intent_node(state: AgentState):
    print("route_after_intent_node ... ")
    intent = state["intent"]
    if "NEW" in intent:
        return "new_project_node"
    elif "MODIFY" in intent:
        return "modify_project_node"
    else:
        return "chat_node"


# ==================== 构造 ====================

project_app_builder = StateGraph(AgentState)
project_app_builder.set_entry_point("intent_node")
project_app_builder.add_node("intent_node", intent_node)
project_app_builder.add_node("new_project_node", new_project_node)
project_app_builder.add_node("modify_project_node", modify_project_node)
project_app_builder.add_node("chat_node", chat_node)

project_app_builder.add_conditional_edges(
    "intent_node",
    route_after_intent_node,
    {
        "new_project_node": "new_project_node",
        "modify_project_node": "modify_project_node",
        "chat_node": "chat_node",
    },
)

project_app_builder.add_edge("new_project_node", END)
project_app_builder.add_edge("modify_project_node", END)
project_app_builder.add_edge("chat_node", END)
