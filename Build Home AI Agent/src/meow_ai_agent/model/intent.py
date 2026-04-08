from langchain_core.documents import Document
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from loguru import logger

import meow_ai_agent.model.base as base
from meow_ai_agent.constants.enums import IntentStatus

# ==================== 意图语义 String ====================

intent_strings = {
    "搜索模块": IntentStatus.WEB.value,
    "工具模块": IntentStatus.TOOL.value,
    "检索模块": IntentStatus.RAG.value,
}

# ==================== 意图语义 LLM ====================

system_prompt_intent = """
你是一个“意图分类器”，负责判断用户当前问题应该走哪种处理方式。

你必须在以下四个类别中选择一个，并且只能输出该类别名称：

WEB / TOOL / RAG / UNKNOW

====================
【分类定义】

WEB：
- 需要实时信息、新闻、时间相关信息
- 或需要联网搜索才能回答
- 示例：
  - “2020年12月1日发生了什么”
  - “今天东京天气如何”
  - “最近AI有什么新进展”

TOOL：
- 用户希望执行操作、控制设备或触发动作
- 通常包含动词（打开、关闭、执行、启动等）
- 示例：
  - “打开卧室灯”
  - “帮我关闭空调”
  - “重启服务器”

RAG：
- 查询已有知识、文档、技术说明、原理解释
- 通常是“是什么 / 为什么 / 如何”
- 示例：
  - “海康摄像头如何重置”
  - “解释一下Transformer”
  - “猫是什么动物”

UNKNOW：
- 闲聊、寒暄、情绪表达
- 无明确意图
- 或无法确定类别
- 示例：
  - “你好”
  - “你在干嘛”
  - “感觉有点累”

====================
【判定规则】

1. 优先判断是否为 TOOL（只要明显是操作指令）
2. 再判断是否需要实时信息（WEB）
3. 再判断是否为知识查询（RAG）
4. 其余全部归为 UNKNOW

====================
【严格要求】

- 只能输出：WEB 或 TOOL 或 RAG 或 UNKNOW
- 不要解释
- 不要输出其他内容
- 不要换行
"""
prompt_intent = ChatPromptTemplate.from_messages([("system", system_prompt_intent), ("placeholder", "{messages}"), ])

# ==================== 意图语义 Semantic Router ====================

intent_docs = [
    # ================= TOOL =================
    Document(page_content="打开灯", metadata={"intent": "TOOL"}),
    Document(page_content="关闭卧室灯", metadata={"intent": "TOOL"}),
    Document(page_content="帮我关掉空调", metadata={"intent": "TOOL"}),
    Document(page_content="把窗户打开", metadata={"intent": "TOOL"}),
    Document(page_content="启动服务器", metadata={"intent": "TOOL"}),
    Document(page_content="重启系统", metadata={"intent": "TOOL"}),
    Document(page_content="关闭电脑", metadata={"intent": "TOOL"}),
    Document(page_content="调高温度", metadata={"intent": "TOOL"}),
    Document(page_content="把灯调暗一点", metadata={"intent": "TOOL"}),
    Document(page_content="执行备份任务", metadata={"intent": "TOOL"}),

    # ================= RAG =================
    Document(page_content="猫是什么动物", metadata={"intent": "RAG"}),
    Document(page_content="解释一下人工智能", metadata={"intent": "RAG"}),
    Document(page_content="为什么天空是蓝色", metadata={"intent": "RAG"}),
    Document(page_content="海康摄像头如何重置", metadata={"intent": "RAG"}),
    Document(page_content="什么是Transformer模型", metadata={"intent": "RAG"}),
    Document(page_content="如何安装docker", metadata={"intent": "RAG"}),
    Document(page_content="Linux如何查看端口", metadata={"intent": "RAG"}),
    Document(page_content="Python中list和tuple的区别", metadata={"intent": "RAG"}),
    Document(page_content="什么是向量数据库", metadata={"intent": "RAG"}),
    Document(page_content="解释一下RAG架构", metadata={"intent": "RAG"}),

    # ================= WEB =================
    Document(page_content="今天东京天气怎么样", metadata={"intent": "WEB"}),
    Document(page_content="现在几点了", metadata={"intent": "WEB"}),
    Document(page_content="最近有什么AI新闻", metadata={"intent": "WEB"}),
    Document(page_content="2024年发生了哪些大事", metadata={"intent": "WEB"}),
    Document(page_content="世界杯什么时候开始", metadata={"intent": "WEB"}),
    Document(page_content="现在比特币价格是多少", metadata={"intent": "WEB"}),
    Document(page_content="今天股市行情如何", metadata={"intent": "WEB"}),
    Document(page_content="最近OpenAI有什么更新", metadata={"intent": "WEB"}),
    Document(page_content="明天会不会下雨", metadata={"intent": "WEB"}),
    Document(page_content="今天新闻头条是什么", metadata={"intent": "WEB"}),

    # ================= UNKNOW =================
    Document(page_content="你好", metadata={"intent": "UNKNOW"}),
    Document(page_content="你在干嘛", metadata={"intent": "UNKNOW"}),
    Document(page_content="今天天气不错啊", metadata={"intent": "UNKNOW"}),
    Document(page_content="哈哈哈", metadata={"intent": "UNKNOW"}),
    Document(page_content="感觉有点无聊", metadata={"intent": "UNKNOW"}),
    Document(page_content="你是谁", metadata={"intent": "UNKNOW"}),
    Document(page_content="可以聊聊天吗", metadata={"intent": "UNKNOW"}),
    Document(page_content="早上好", metadata={"intent": "UNKNOW"}),
    Document(page_content="晚安", metadata={"intent": "UNKNOW"}),
    Document(page_content="嗯好的", metadata={"intent": "UNKNOW"}),
]

base.vectorstore_intent_router.add_documents(intent_docs)


# ==================== 额外方法 ====================

def llm_classify(query: str):
    # 内部小模型，不流式
    ret = base.llm_l.invoke(
        prompt_intent.format_messages(
            messages=[HumanMessage(content=query)]
        )
    ).content.strip().upper()
    logger.info(f"Classify result: {ret}")
    if ret not in ["WEB", "TOOL", "RAG", "UNKNOW"]:
        return "UNKNOW"
    return ret


# ==================== 节点定义 ====================

def intent_single_node(state: base.AgentState):
    """确定输入语义，单次对话确定意图后不再更改，方便测试子功能"""
    messages = state["messages"]
    logger.info(f"Intent messages: {messages}")
    query = messages[-1].content
    logger.info(f"Intent query: {query}")
    if state.get("intent"):
        logger.info(f"Intent intent: {state['intent']}")
        return {}
    # String 先判断
    logger.info(f"No intent for query")
    for intent_str_key in intent_strings:
        if intent_str_key in query:
            logger.info(f"Intent {intent_str_key}")
            return {"intent": intent_strings[intent_str_key], "intent_force": True}
    # Embedding 再判断
    results = base.qdrant_cli.query_points(
        collection_name=base.intent_router,
        query=base.emb.embed_query(query),
        limit=3
    )
    if not results:
        return {"intent": llm_classify(query)}

    logger.info(f"Intent results: {results}")
    top = results.points[0]
    intent = top.payload["metadata"]["intent"]
    score = top.score

    logger.info(f"Intent: {intent}, score: {score}")
    if score >= 0.65:
        return {"intent": intent}

    # LLM 保底
    return {"intent": llm_classify(query)}
