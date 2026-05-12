import json
from collections import deque
from enum import Enum
from typing import TypedDict, Annotated, List, Optional

import redis
from flask import Flask, Response, request
from flask import jsonify
from langchain_community.chat_models import ChatOpenAI
from langchain_core.messages import AIMessage
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_ollama import ChatOllama
from langgraph.checkpoint.redis import RedisSaver
from langgraph.constants import END
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages

redis_cli = redis.Redis(host='localhost', port=6379)

llm = ChatOllama(
    model="qwen2.5:1.5b",
    base_url="http://localhost:11434",
)

llm_no_stream = ChatOpenAI(
    model="qwen3.5-flash",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key="key",
    tags=["nostream"],
    extra_body={
        "enable_thinking": False,
    }
)



# ================================================================

# 简化流程直接写死图片分析，不再接入图片模型
image_desc = {
    "背景图片1": "多层酒架陈列各式酒瓶，暖光营造复古温馨氛围。适用推广项目：酒类（高端酒品、调酒课程）、餐饮服务。",
    "背景图片2": "温馨书房，四周高大木质书架满载书籍，中央深色皮质扶手椅与棕色单人椅，木质地板配地毯，射灯营造静谧阅读氛围。适用推广项目：书籍、家居装饰。",
    "背景图片3": "图片展示温馨简约的客厅，米色沙发搭毛毯，圆形木茶几置绿植，大窗户透入自然光，搭配龟背竹等绿植与米色窗帘，营造自然舒适氛围。适用推广项目：家居装饰、绿植、软装设计。",
    "背景图片4": "白色沙滩绵延，清澈蓝绿色海水轻拍岸边，棕榈树与远山相映，蓝天白云点缀，呈现热带海滨度假胜地。适用推广项目：旅游、海岛游、度假酒店。",
    "背景图片5": "金色沙丘在柔和光线中延展，细腻波纹如丝绸般流动，沙丘起伏间透出沙漠的静谧与壮美。适用推广：户外探险装备、摄影器材、防晒护肤产品、沙漠旅游线路。",
    "背景图片6": "宽敞明亮的健身房内，多台跑步机整齐排列，搭配动感单车等器械，工业风装修，裸露管道与大窗户采光充足。推广项目：健身器材、运动服饰、健康科技产品（如智能手环）。",
    "背景图片7": "霓虹紫蓝灯光照亮复古街机厅，排列整齐的街机、涂鸦墙面与格子地板，营造赛博朋克风游戏空间。推广项目：数码（游戏机/电竞设备）、娱乐（复古游戏周边）。",
    "背景图片8": "蓝天白云下，广袤绿草地缀满白、黄、橙等小花，生机盎然。推广项目：美妆（天然草本护肤）。",
    "背景图片9": "粉色樱花树成排，石板路蜿蜒绿草间，春意盎然。适合旅游推广（赏樱之旅）、摄影器材（樱花主题拍摄）及文创产品（樱花周边）。",
    "背景图片10": "儿童房内设彩色条纹与米色帐篷，内有毛绒玩具；墙面挂艺术画、动物挂饰，地面铺编织地毯，配木质玩具架及毛绒玩具篮，整体温馨童趣。推广项目：母婴、儿童玩具、家居装饰。",
    "人物图片1": "男子身着浅色汉服，束发持折扇，背景水墨植物与书法点缀，古风雅致。适用推广项目：服装（国风/汉服类）",
    "人物图片2": "蓝发人物戴发光耳机，银色科技外套嵌蓝色光效，赛博朋克未来风。推广：数码、游戏、潮玩、智能穿戴设备。",
    "人物图片3": "图片中老人白发编辫，头戴羽毛装饰，身着红蓝民族服饰，佩戴银饰与蓝宝石项链，展现传统民族风貌。适用推广项目：民族服饰、文化旅游、手工艺品。",
    "人物图片4": "人物面部颈部饰金色几何纹身，配大圆环耳饰与金属颈饰，灰底凸显未来部落风。适配美妆（纹身灵感彩妆）及数码（科技设计）推广项目。",
    "人物图片5": "黑白老照片中，男士身着复古西装、领结，叼烟斗，发型整齐，背景素色。推广项目：男士服装（复古西装、绅士服饰）。",
    "人物图片6": "粉色双马尾配黑色发饰，烟熏眼妆精致，身着黑色皮质紧身胸衣与白色蕾丝袖，颈间金属链项圈点缀，整体呈现哥特暗黑风。适用推广项目：美妆（妆容）、服装（哥特风服饰）。",

}


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
    extra: Optional[str]
    parse_reason: Optional[str]


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    project: Optional[Project]
    created_project: Optional[bool]
    avatar_list: Optional[List[ProjectItem]]
    product_list: Optional[List[ProjectItem]]
    bg_list: Optional[List[ProjectItem]]
    is_confirm: Optional[bool]
    project_res: Optional[str]
    loaded_res: Optional[bool]


confirm_words = [
    "是", "好的", "确认", "ok", "yes", "sure", "嗯", "可以", "行", "是的", "确定", "好", "没问题",
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

system_prompt_main = """
你是需求解析专家。从用户输入中提取推广项目（通常包含期望项目的场景、风格、内容等信息），只输出纯JSON，不要包含代码，不要其他内容。

{history_project}

输出格式：
{{
  "is_success": true/false （是否成功解析到具体的项目）,
  "style": "内容风格描述，没有相关描述则可以根据自己理解以及推荐填写",
  "budget": 预算数字（元，取整数）没有预算相关描述，或者无预算上限，则为-1,
  "audience": "目标人群描述，没有相关描述则为空",
  "scene": "使用/展示场景，没有相关描述则为空",
  "tone": "主持人语气/语调，没有相关描述则为空",
  "keywords": ["关键词1", "关键词2"],
  "extra": "其他输入补充信息，以及无法归类的推广项目调整信息",
  "parse_reason": "解析思路说明"
}}

只输出纯JSON，不要包含代码，不要其他内容。
"""
prompt_main = ChatPromptTemplate.from_messages([("system", system_prompt_main), ("placeholder", "{messages}"), ])

system_prompt_select = """
你是产品项目设计师，专门负责资源选型。从给定虚拟人物形象资源列表，以及产品列表，以及背景图片资源列表中，
根据用户的对于期望推广项目的描述，选择一个合适的虚拟人物以及一个背景图片以及1-3个推广产品，并且输出相应推广脚本，只输出纯JSON，不要包含代码，不要其他内容。

可选择的虚拟人物有：

{avatar_list_desc}

可选择的产品有：

{product_list_desc}

可选择的背景图片有：

{bg_list_desc}

输出格式：
{{
  "avatar": "选择的虚拟人物的图片名称",
  "avatar_reason": "选择该虚拟人物的原因",
  "bg": "选择的背景图片的名称",
  "bg_reason": "选择该背景图片的原因",
  "products": [
    {{
    "name": "选择的推广产品的名称",
    "reason": "选择该推广产品的原因"
    }},
    ...
  ],
  "script": "根据选择的虚拟人物以及背景和推广产品，设计的推广脚本内容，要求包含推广要点，且适合主播口播，500字左右，不要换行。"
}}

只输出纯JSON，不要包含代码，不要其他内容。
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


# ==================== 节点定义 ====================

def confirm_node(state: AgentState):
    print("confirm_node ...")
    has_project = state.get("created_project") and state.get("project") is not None and state.get("project").get(
        "script") is not None
    loaded_res = state.get("loaded_res")
    if not has_project or not loaded_res:
        return {}
    # 字符串判断
    print("confirm_node ... check confirm")
    text = state["messages"][-1].content.lower()
    if text in confirm_words:
        return {"is_confirm": True}
    # LLM 保底
    result = llm_no_stream.invoke(
        prompt_confirm.format_messages(
            messages=[HumanMessage(content=text)]
        )
    ).content.strip().upper()
    print(f"confirm classify result: {result}")
    if "YES" in result:
        return {"is_confirm": True}
    else:
        return {}


def project_parse_node(state: AgentState):
    print("new_project_parse_node ... ")
    last_msg = state["messages"][-1].content
    has_project = state.get("created_project") and state.get("project") is not None
    if has_project:
        project = state["project"]
        budget = project.get("budget")
        style = project.get("style")
        audience = project.get("audience")
        scene = project.get("scene")
        tone = project.get("tone")
        keywords = project.get("keywords")
        extra = project.get("extra")
        history_project_section = (
            f"基于之前项目：预算: {budget if budget != -1 else '无限制'} 元, 风格: {style or '无'},"
            f" 受众: {audience or '无'}, 场景: {scene or '无'}, 语气: {tone or '无'}, "
            f"关键词: {', '.join(keywords) if keywords else '无'}，其他补充信息: {extra or '无'}")
    else:
        history_project_section = ""
    print(f"history_project_section: {history_project_section}")
    messages = prompt_main.format_messages(
        history_project=history_project_section,
        messages=[HumanMessage(content=last_msg)]
    )
    parse_json = llm_no_stream.invoke(messages).content
    print(f"parse_json_data: {parse_json}")
    parse_json_data = json.loads(parse_json)
    is_success = parse_json_data.get("is_success")
    if is_success:
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
        }, "created_project": True}
    else:
        project = state.get("project")
        if project is None:
            project = {}
        project["parse_reason"] = parse_json_data.get("parse_reason")
        return {"project": project, "created_project": False}


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
        for item in bg_list:
            item_name = item.get("name")
            if item_name and image_desc.get(item_name):
                item["desc"] = image_desc.get(item_name)
            else:
                raise ValueError("输入图片无法查询到默认描述")
        for item in avatar_list:
            item_name = item.get("name")
            if item_name and image_desc.get(item_name):
                item["desc"] = image_desc.get(item_name)
            else:
                raise ValueError("输入图片无法查询到默认描述")
        return {
            "bg_list": bg_list,
            "product_list": product_list,
            "avatar_list": avatar_list,
            "loaded_res": True,
        }
    except Exception as e:
        print(f"load_res_pre_node error: {e}")
    return {
        "messages": [
            AIMessage(content="图片资源解析错误，请确认图片相关资源格式正确性，且不能为空\n\n")
        ]
    }


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
    avatar_list_desc = "\n\n".join(
        [f"虚拟人物的图片名称：{item['name']}，描述：{item.get('desc', '无描述')}" for item in avatar_list])
    product_list_desc = "\n\n".join(
        [f"产品名称：{item['name']}，价格：{item.get('price', '无明确价格')} 元" for item in product_list])
    bg_list_desc = "\n\n".join([f"背景图片名称：{item['name']}，描述：{item.get('desc', '无描述')}" for item in bg_list])

    # 准备项目描述
    project_desc = (f"预算: {budget if budget != -1 else '无限制'}, 风格: {style or '无'},"
                    f" 受众: {audience or '无'}, 场景: {scene or '无'}, 语气: {tone or '无'}, "
                    f"关键词: {', '.join(keywords) if keywords else '无'}，其他补充信息: {extra or '无'}")

    # 格式化消息
    messages = prompt_select.format_messages(
        avatar_list_desc=avatar_list_desc,
        product_list_desc=product_list_desc,
        bg_list_desc=bg_list_desc,
        messages=[HumanMessage(content=f"项目描述: \n\n {project_desc}")]
    )

    print(messages)

    # 调用 LLM
    response = llm_no_stream.invoke(messages).content

    print(f"Output json: {response}")

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


**选择理由：{prod.get("reason", "")}**
"""

    output_message = f"""
## 推广项目构建参考


### 虚拟人物选择


<img src="{avatar_item.get("url", "")}" width="40%">


**选择理由：{avatar_item.get("reason", "") if avatar_item else "无"}**



### 背景选择


<img src="{bg_item.get("url", "")}" width="40%">


**选择理由：{bg_item.get("reason", "") if bg_item else "无"}**



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


def project_output_node(state: AgentState):
    print("project_output_node ... ")
    project = state["project"]
    avatar = project["avatar"]
    bg = project["background"]
    product = project["products"]
    script = project["script"]

    print(f"project_output_node data {project} {avatar} {bg} {script} {product}")

    products_section = ""
    for prod in product:
        products_section += f"""{prod["name"]} {prod.get("price", "无")} 元，"""
    products_section = products_section[:-1]

    project_finish_msg = f"""
## 最终项目生成结果


### 虚拟人物选择


<img src="{avatar["url"]}" width="40%">


### 背景选择


<img src="{bg["url"]}" width="40%">


### 商品选择


{products_section}


### 推广脚本


{script}


**您可用重新配置虚拟人物资源、商品资源以及背景资源，然后提供新的推广需求，我将再次为您生成新的推广项目。**

"""
    return {
        "project": None,
        "created_project": None,
        "avatar_list": None,
        "product_list": None,
        "bg_list": None,
        "is_confirm": None,
        "project_res": None,
        "loaded_res": None,
        "messages": [
            AIMessage(content=project_finish_msg)
        ]
    }


# ==================== 路由定义 ====================

def route_after_confirm_node(state: AgentState):
    print("route_after_confirm_node ... ")
    if state.get("is_confirm"):
        return "project_output_node"
    else:
        return "project_parse_node"


def route_after_project_parse_node(state: AgentState):
    print("route_after_project_parse_node ... ")
    if not state.get("created_project"):
        return "project_parse_fail_node"
    if not state.get("loaded_res"):
        return "load_res_pre_node"
    else:
        return "select_res_node"


def route_after_load_res_pre_node(state: AgentState):
    print("route_after_load_res_pre_node ... ")
    if state.get("loaded_res"):
        return "select_res_node"
    else:
        return END


# ==================== 构造 ====================

project_app_simple_builder = StateGraph(AgentState)

project_app_simple_builder.add_node("confirm_node", confirm_node)
project_app_simple_builder.add_node("project_output_node", project_output_node)
project_app_simple_builder.add_node("project_parse_node", project_parse_node)
project_app_simple_builder.add_node("project_parse_fail_node", project_parse_fail_node)
project_app_simple_builder.add_node("select_res_node", select_res_node)
project_app_simple_builder.add_node("load_res_pre_node", load_res_pre_node)

project_app_simple_builder.set_entry_point("confirm_node")

project_app_simple_builder.add_conditional_edges(
    "confirm_node",
    route_after_confirm_node,
    {
        "project_parse_node": "project_parse_node",
        "project_output_node": "project_output_node",
    }
)

project_app_simple_builder.add_conditional_edges(
    "project_parse_node",
    route_after_project_parse_node,
    {
        "project_parse_fail_node": "project_parse_fail_node",
        "load_res_pre_node": "load_res_pre_node",
        "select_res_node": "select_res_node",
    }
)

project_app_simple_builder.add_conditional_edges(
    "load_res_pre_node",
    route_after_load_res_pre_node,
    {
        "select_res_node": "select_res_node",
        END: END,
    }
)

project_app_simple_builder.add_edge("project_parse_fail_node", END)
project_app_simple_builder.add_edge("select_res_node", END)
project_app_simple_builder.add_edge("project_output_node", END)


# ================================================================


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


system_prompt_chat = """
你是一个聊天机器人，需要遵守以下规则：
1. 亲切礼貌，不卑不亢。
2. 乐于给出建议。
"""

prompt_chat = ChatPromptTemplate.from_messages([("system", system_prompt_chat), ("placeholder", "{messages}"), ])


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
project_app_simple = project_app_simple_builder.compile(checkpointer=memory)

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
    model = request.args.get('model')
    project_res = request.args.get('project_res')

    print(f"start stream {session_id} {user_input}")

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

    def generateProjectNoStream():
        thread_config = {"configurable": {"thread_id": session_id}}
        message = HumanMessage(content=user_input)

        print(f"start generateProjectNoStream {session_id} {user_input}")

        try:
            for chunk in project_app_simple.stream(
                    {"messages": [message], "project_res": project_res},
                    config=thread_config,
                    stream_mode="messages"
            ):
                msg_chunk, metadata = chunk
                if not msg_chunk.content:
                    continue
                yield f"data: {msg_chunk.content}\n"

            yield "data: [[DONE]]\n"

        except Exception as e:
            import traceback
            traceback.print_exc()
            yield f"data: [[ERROR]] {str(e)}\n"

    if model == "PROJECT":
        ret = Response(generateProjectNoStream(), content_type='text/event-stream')
    else:
        ret = Response(generate(), content_type='text/event-stream')

    return ret


if __name__ == '__main__':
    app.run()
