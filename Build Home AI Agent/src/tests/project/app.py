import json
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
    budget: Optional[int]
    style: Optional[str]
    audience: Optional[str]
    scene: Optional[str]
    tone: Optional[str]
    keywords: Optional[List[str]]
    parse_reason: Optional[str]


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    intent: Optional[str]
    project: Optional[Project]
    avatar_list: Optional[List[ProjectItem]]
    product_list: Optional[List[ProjectItem]]
    bg_list: Optional[List[ProjectItem]]
    is_confirm: Optional[bool]


system_prompt_main = """
你是需求解析专家。从用户输入中提取项目需求，输出 JSON。

{history_project}

输出格式：
{{
  "is_success": true/false （是否成功解析到具体的项目）,
  "style": "内容风格描述，没有相关描述则为空",
  "budget": 预算数字（元，取整数）没有预算相关描述，或者无预算上限，则为-1,
  "audience": "目标人群描述，没有相关描述则为空",
  "scene": "使用/展示场景，没有相关描述则为空",
  "tone": "主持人语气/语调，没有相关描述则为空",
  "keywords": ["关键词1", "关键词2"],
  "parse_reason": "解析思路说明"
}}

只输出 JSON，不要其他内容。
"""
prompt_main = ChatPromptTemplate.from_messages([("system", system_prompt_main), ("placeholder", "{messages}"), ])

# ==================== 额外方法 ====================




# ==================== 节点定义 ====================


def project_parse_node(state: AgentState):
    print("new_project_parse_node ... ")
    last_msg = state["messages"][-1].content
    has_project = state.get("project") is not None
    if has_project:
        history_project_section = f"基于之前项目：\n{json.dumps(state.get("project"), ensure_ascii=False)}"
    else:
        history_project_section = ""
    print("=====================")
    print(history_project_section)
    print("=====================")
    messages = prompt_main.format_messages(
        history_project=history_project_section,
        messages=[HumanMessage(content=last_msg)]
    )
    parse_json = llm_text.invoke(messages).content
    parse_json_data = json.loads(parse_json)
    return {"project": {
        "background": None,
        "avatar": None,
        "products": [],
        "script": None,
        "budget": parse_json_data.get("budget"),
        "style": parse_json_data.get("style"),
        "audience": parse_json_data.get("audience"),
        "scene": parse_json_data.get("scene"),
        "tone": parse_json_data.get("tone"),
        "keywords": parse_json_data.get("keywords"),
        "parse_reason": parse_json_data.get("parse_reason"),
    }}

def new_project_node(state: AgentState):
    print("new_project_node ... ")
    print(state["project"])
    return {
        "messages": [
            AIMessage(content="新需求分析完成")
        ]
    }


# ==================== 路由定义 ====================



# ==================== 输出节点 ====================

stream_output_list = ["project_parse_node"]

# ==================== 构造 ====================

project_app_builder = StateGraph(AgentState)
project_app_builder.set_entry_point("project_parse_node")
project_app_builder.add_node("project_parse_node", project_parse_node)

project_app_builder.add_edge("project_parse_node", END)
