import base64
import json
from typing import TypedDict, Annotated, List, Optional

import requests
from langchain_core.messages import AIMessage
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langgraph.constants import END
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages

llm_text = ChatOllama(model="qwen3:14b-q4_K_M", base_url="http://localhost:11434", temperature=0.3)
llm_text_no_stream = ChatOllama(model="qwen3:14b-q4_K_M", base_url="http://localhost:11434", temperature=0.3, tags=["nostream"],)
llm_vl = ChatOllama(model="qwen3-vl:8b", base_url="http://localhost:11434", temperature=0.2, tags=["nostream"], )


class ProjectItem(TypedDict):
    name: Optional[str]
    url: Optional[str]
    price: Optional[float]
    desc: Optional[str]
    described: Optional[bool]
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
    extra: Optional[str]
    parse_reason: Optional[str]


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    intent: Optional[str]
    project: Optional[Project]
    created_project: Optional[bool]
    avatar_list: Optional[List[ProjectItem]]
    product_list: Optional[List[ProjectItem]]
    bg_list: Optional[List[ProjectItem]]
    loaded_res: Optional[bool]
    is_confirm: Optional[bool]
    project_res: Optional[str]


system_prompt_main = """
你是需求解析专家。从用户输入中提取推广项目（通常包含期望项目的场景、风格、内容等信息），输出 JSON。

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
  "extra": "其他补充信息",
  "parse_reason": "解析思路说明"
}}

只输出 JSON，不要其他内容。
"""
prompt_main = ChatPromptTemplate.from_messages([("system", system_prompt_main), ("placeholder", "{messages}"), ])

system_prompt_select = """
你是产品项目设计师，专门负责资源选型。从给定虚拟人物形象资源列表，以及产品列表，以及背景图片资源列表中，
根据用户的对于期望推广项目的描述，选择一个合适的虚拟人物，以及一个背景图片，以及1-3个推广产品，并且配合推广脚本，输出 JSON。

{avatar_list_desc}

{product_list_desc}

{bg_list_desc}

输出格式：
{{
  "avatar": "选择的虚拟人物的图片名称",
  "avatar_reason": "选择该虚拟人物的原因",
  "bg": "选择的虚拟人物的图片名称",
  "bg_reason": "选择该背景图片的原因",
  "products": [
    {{
    "name": "选择的推广产品的名称",
    "reason": "选择该推广产品的原因"
    }},
    ...
  ],
  "script": "根据选择的资源，设计的推广脚本内容，要求包含推广要点，且适合主播口播，500字左右"
}}

只输出 JSON，不要其他内容。
"""
prompt_select = ChatPromptTemplate.from_messages([("system", system_prompt_select), ("placeholder", "{messages}"), ])

system_prompt_image = """
你是一个专门处理图片的机器人。描述你看到的图片，以及可能适用的推广项目类型（如：美妆、数码、服装等）（总共100字以内，不需要标明具体字数）。
"""
prompt_image = ChatPromptTemplate.from_messages([
    ("system", system_prompt_image),
    ("human", [
        {"type": "text", "text": "请描述这张图片："},
        {"type": "image_url", "image_url": {"url": "{image_url}"}}
    ])
])

# ==================== 额外方法 ====================

def image_url_to_base64(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        img_base64 = base64.b64encode(response.content).decode('utf-8')
        return img_base64
    except requests.RequestException as e:
        print(f"请求失败: {e}")
        return None


# ==================== 节点定义 ====================


def project_parse_node(state: AgentState):
    print("new_project_parse_node ... ")
    last_msg = state["messages"][-1].content
    has_project = state.get("created_project") and state.get("project") is not None
    if has_project:
        history_project_section = f"基于之前项目：\n{json.dumps(state.get("project"), ensure_ascii=False)}"
    else:
        history_project_section = ""
    print(f"history_project_section: {history_project_section}")
    messages = prompt_main.format_messages(
        history_project=history_project_section,
        messages=[HumanMessage(content=last_msg)]
    )
    parse_json = llm_text.invoke(messages).content
    parse_json_data = json.loads(parse_json)
    print(f"parse_json_data: {parse_json_data}")
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
        "extra": parse_json_data.get("extra"),
        "parse_reason": parse_json_data.get("parse_reason"),
    }, "created_project": parse_json_data.get("is_success")}


def project_parse_fail_node(state: AgentState):
    print("project_parse_fail_node ... ")
    return {
        "messages": [
            AIMessage(content="项目创建失败，" + state["project"].get("parse_reason"))
        ]
    }


def load_res_pre_node(state: AgentState):
    print("load_res_pre_node ... ")
    try:
        json_obj = json.loads(state["project_res"])
        bg_list = json_obj.get("bgList")
        product_list = json_obj.get("productList")
        avatar_list = json_obj.get("avatarList")
        if not bg_list or not product_list or not avatar_list:
            return {
                "messages": [
                    AIMessage(content="资源检测为空，请检查虚拟人物、商品、背景是否配置\n\n")
                ]
            }
        return {
            "bg_list": bg_list,
            "product_list": product_list,
            "avatar_list": avatar_list,
            "messages": [
                AIMessage(content="图片资源尚未解析，即将解析传入的图片资源...\n\n")
            ]
        }
    except Exception as e:
        print(f"load_res_pre_node error: {e}")
    return {
        "messages": [
            AIMessage(content="图片资源解析错误，请确认图片相关资源格式正确性，且不能为空\n\n")
        ]
    }


def load_res_node(state: AgentState):
    print("load_res_node ... ")
    bg_list = state["bg_list"]
    avatar_list = state["avatar_list"]
    lists_to_process = [
        ("bg_list", bg_list),
        ("avatar_list", avatar_list),
    ]
    for list_name, item_list in lists_to_process:
        for i, item in enumerate(item_list):
            print(f"load_res_node {item}")
            if not item.get("described"):
                item["described"] = True
                if item.get("url"):
                    try:
                        b64 = f"data:image/jpeg;base64,{image_url_to_base64(item["url"])}"
                        chain = prompt_image | llm_vl
                        response = chain.invoke({"image_url": b64})
                        description = response.content.strip()
                        item["desc"] = description
                        return {
                            "messages": [
                                AIMessage(content=f"对于【{item["name"]}】解析：\n\n\n {description}\n\n")
                            ]
                        }
                    except Exception as e:
                        error_msg = f"对于【{item["name"]}】解析：\n\n\n 失败: {str(e)}"
                        item["desc"] = "图片分析失败"
                        return {"messages": [AIMessage(content=error_msg)]}
                return {"messages": [AIMessage(content=f"对于【{item["name"]}】解析：\n\n\n 无法获取图片")]}
    return {"loaded_res": True}



def select_res_node(state: AgentState):
    print("select_res_node ... ")
    bg_list = state["bg_list"]
    avatar_list = state["avatar_list"]
    product_list = state["product_list"]

    budget = state["project"].get("budget")
    style = state["project"].get("style")
    audience = state["project"].get("audience")
    scene = state["project"].get("scene")
    tone = state["project"].get("tone")
    keywords = state["project"].get("keywords")
    extra = state["project"].get("extra")

    # 构建资源描述
    avatar_list_desc = "\n".join([f"- {item['name']}: {item.get('desc', '无描述')}" for item in avatar_list])
    product_list_desc = "\n".join([f"- {item['name']}: {item.get('desc', '无描述')}" for item in product_list])
    bg_list_desc = "\n".join([f"- {item['name']}: {item.get('desc', '无描述')}" for item in bg_list])

    # 准备项目描述
    project_desc = (f"预算: {budget if budget != -1 else '无限制'}, 风格: {style or '无'},"
                    f" 受众: {audience or '无'}, 场景: {scene or '无'}, 语气: {tone or '无'}, "
                    f"关键词: {', '.join(keywords) if keywords else '无'}，其他补充信息: {extra or '无'}")

    # 格式化消息
    messages = prompt_select.format_messages(
        avatar_list_desc=avatar_list_desc,
        product_list_desc=product_list_desc,
        bg_list_desc=bg_list_desc,
        messages=[HumanMessage(content=f"项目描述: {project_desc}")]
    )

    # 调用 LLM
    response = llm_text_no_stream.invoke(messages).content
    json_data = json.loads(response)

    # 脚本
    script = json_data["script"]

    # 查找并设置 avatar
    avatar_name = json_data.get("avatar")
    avatar_item = next((item for item in avatar_list if item["name"] == avatar_name), None)
    if avatar_item:
        avatar_item["reason"] = json_data.get("avatar_reason")

    # 查找并设置 background
    bg_name = json_data.get("bg")
    bg_item = next((item for item in bg_list if item["name"] == bg_name), None)
    if bg_item:
        bg_item["reason"] = json_data.get("bg_reason")

    # 查找并设置 products
    products_selected = []
    for prod in json_data.get("products", []):
        prod_name = prod["name"]
        prod_item = next((item for item in product_list if item["name"] == prod_name), None)
        if prod_item:
            prod_item["reason"] = prod["reason"]
            products_selected.append(prod_item)

    # 更新 project
    updated_project = state["project"].copy()
    updated_project["avatar"] = avatar_item
    updated_project["background"] = bg_item
    updated_project["script"] = script
    updated_project["products"] = products_selected

    # 构建商品选择部分
    products_section = ""
    for prod in products_selected:
        products_section += f"""
#### {prod["name"]}


商品价格：{prod.get("price", "无")} 元


**选择理由：{prod["reason"]}**
"""

    output_message = f"""
## 推广项目构建参考


### 虚拟人物选择


<img src="{avatar_item["url"]}" width="40%">


人物描述：{avatar_item["desc"] if avatar_item else "无"}


**选择理由：{avatar_item["reason"] if avatar_item else "无"}**



### 背景选择


<img src="{bg_item["url"]}" width="40%">


背景描述：{bg_item["desc"] if bg_item else "无"}


**选择理由：{bg_item["reason"] if bg_item else "无"}**



### 商品选择


{products_section}



### 推广脚本


{script}



**是否确认生成该推广项目？**


"""

    return {
        "project": updated_project,
        "messages": [
            AIMessage(content=output_message)
        ]
    }


# ==================== 路由定义 ====================

def route_after_project_parse_node(state: AgentState):
    print("route_after_project_parse_node ... ")
    if not state.get("created_project"):
        return "project_parse_fail_node"
    if not state.get("loaded_res"):
        return "load_res_pre_node"
    else:
        return "select_res_node"


def route_after_load_res_node(state: AgentState):
    print("route_after_load_res_node ... ")
    if state.get("loaded_res"):
        return "select_res_node"
    else:
        return "load_res_node"


# ==================== 输出节点 ====================

stream_output_list = ["project_parse_fail_node", "load_res_pre_node", "load_res_node", "select_res_node"]

# ==================== 构造 ====================

project_app_builder = StateGraph(AgentState)
project_app_builder.add_node("project_parse_node", project_parse_node)
project_app_builder.add_node("project_parse_fail_node", project_parse_fail_node)
project_app_builder.add_node("load_res_pre_node", load_res_pre_node)
project_app_builder.add_node("load_res_node", load_res_node)
project_app_builder.add_node("select_res_node", select_res_node)

project_app_builder.set_entry_point("project_parse_node")

project_app_builder.add_conditional_edges(
    "project_parse_node",
    route_after_project_parse_node,
    {
        "project_parse_fail_node": "project_parse_fail_node",
        "load_res_pre_node": "load_res_pre_node",
        "select_res_node": "select_res_node",
    }
)

project_app_builder.add_conditional_edges(
    "load_res_node",
    route_after_load_res_node,
    {
        "load_res_node": "load_res_node",
        "select_res_node": "select_res_node"
    }
)

project_app_builder.add_edge("load_res_pre_node", "load_res_node")


project_app_builder.add_edge("project_parse_fail_node", END)
project_app_builder.add_edge("select_res_node", END)
