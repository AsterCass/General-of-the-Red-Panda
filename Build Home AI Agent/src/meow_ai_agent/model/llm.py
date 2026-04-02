import re
from typing import TypedDict, Annotated, Optional

from langchain_core.documents import Document
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_ollama import OllamaEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import END
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from loguru import logger
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

import meow_ai_agent.constants.env as env
from meow_ai_agent.utils.device import turn_off_light_bedroom, turn_off_light_living_room, close_window_living_room, \
    turn_on_heating_bedroom, open_curtain_living_room, close_curtain_living_room


# ==================== 节点状态 ====================

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]  # 自动合并消息历史
    pending_action: Optional[AIMessage] | None
    confirmed: Optional[bool] | None


# ==================== 模型 ====================

llm = ChatOllama(
    model=env.MODEL_NAME,
    base_url=env.OLLAMA_BASE_URL,
)

emb = OllamaEmbeddings(
    model=env.EMBED_TEXT_MODEL_NAME,
    base_url=env.OLLAMA_BASE_URL
)

llm_l = ChatOllama(
    model=env.MODEL_NAME_LIGHT,
    base_url=env.OLLAMA_BASE_URL,
    temperature=0
)

# ==================== 语义确认（临时） ====================

confirm_words = [
    "是", "好的", "确认", "ok", "yes", "sure", "嗯", "可以", "行", "行", "是的", "确定"
]

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

# ==================== 工具配置 ====================

tools = [turn_off_light_bedroom, turn_off_light_living_room, close_window_living_room,
         turn_on_heating_bedroom, open_curtain_living_room, close_curtain_living_room]
tool_node = ToolNode(tools=tools)
tool_map = {t.name: t for t in tools}
llm_with_tools = llm.bind_tools(tools)

# ==================== 模型配置 ====================

system_prompt = """
你是一个智能家居助手，必须严格遵守以下规则：
0. 你叫由乃。
1. 工具调用必须通过系统提供的 function calling 机制完成。
2. 当需要执行设备或者工具操作时，必须使用 tool_call，不允许模拟 tool_call ，不允许在文本中输出 JSON
3. 如果不能调用工具，就正常回答.
4. 不要自问自答。
"""
prompt = ChatPromptTemplate.from_messages([("system", system_prompt), ("placeholder", "{messages}"), ])

# ==================== 文档切分 ====================

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

# ==================== 向量库 ====================

qdrant_cli = QdrantClient(
    url=env.QDRANT_URL
)
collection_name = "knowledge_base"

# 临时测试，每次清空
if qdrant_cli.collection_exists(collection_name):
    qdrant_cli.delete_collection(collection_name)

if not qdrant_cli.collection_exists(collection_name):
    qdrant_cli.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=1024,
            distance=Distance.COSINE
        )
    )

vectorstore = QdrantVectorStore(
    client=qdrant_cli,
    collection_name=collection_name,
    embedding=emb
)

# ==================== 检索器 ====================

retriever = vectorstore.as_retriever(
    search_kwargs={
        "k": 3
    }
)

# ==================== 测试 ====================

docs = [
    Document(page_content="猫是哺乳动物，通常被当作宠物饲养。", metadata={"source": "wiki"}),
    Document(page_content="狗是人类最好的朋友，常用于看家护院。", metadata={"source": "wiki"}),
    Document(page_content="猫喜欢独处，性格相对独立。", metadata={"source": "wiki"}),
    Document(page_content="狗通常性格忠诚，喜欢与人互动。", metadata={"source": "wiki"}),
    Document(page_content="猫属于食肉动物，主要捕食小型动物。", metadata={"source": "wiki"}),
    Document(page_content="狗经过人类长期驯化，是典型的家养动物。", metadata={"source": "wiki"}),
    Document(page_content="老虎也是猫科动物，但体型巨大且危险。", metadata={"source": "wiki"}),
    Document(page_content="狼是狗的近亲，生活在野外环境中。", metadata={"source": "wiki"}),
    Document(page_content="猫的听觉非常敏锐，可以捕捉微小声音。", metadata={"source": "wiki"}),
    Document(page_content="狗的嗅觉非常灵敏，常用于搜救和侦查。", metadata={"source": "wiki"}),
    Document(page_content="猫每天会花很多时间进行自我清洁。", metadata={"source": "wiki"}),
    Document(page_content="狗需要每天外出活动，否则容易焦虑。", metadata={"source": "wiki"}),
    Document(page_content="猫科动物通常具有锋利的爪子和牙齿。", metadata={"source": "wiki"}),
    Document(page_content="犬科动物通常具有群居行为。", metadata={"source": "wiki"}),
    Document(page_content="猫的夜视能力很强，适合夜间活动。", metadata={"source": "wiki"}),
    Document(page_content="狗可以通过训练完成复杂指令。", metadata={"source": "wiki"}),
    Document(page_content="汽车是一种交通工具，用于人类出行。", metadata={"source": "wiki"}),
    Document(page_content="飞机可以在空中飞行，是长途交通方式。", metadata={"source": "wiki"}),
    Document(page_content="计算机可以执行复杂计算，是现代科技核心。", metadata={"source": "wiki"}),
    Document(page_content="苹果是一种水果，富含维生素。", metadata={"source": "wiki"}),
]

split_docs = splitter.split_documents(docs)
vectorstore.add_documents(split_docs)

ret1 = retriever.invoke("猫是什么动物")
ret2 = retriever.invoke("什么动物嗅觉好")
ret3 = retriever.invoke("交通工具有哪些")

for r in ret1:
    print(r.page_content)

for r in ret2:
    print(r.page_content)

for r in ret3:
    print(r.page_content)

# ==================== 节点定义 ====================

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
    if text in confirm_words:
        return {"confirmed": True}
    # 小模型兜底
    result = llm_l.invoke(
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


# ==================== 路由定义 ====================

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


# ==================== 流转图绘制 ====================

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

# ==================== 编译 ====================
# todo 替换为 redis 或者其他
memory = MemorySaver()
app = builder.compile(checkpointer=memory)
