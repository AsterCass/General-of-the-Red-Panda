import os

from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_qdrant import QdrantVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from loguru import logger
from qdrant_client.models import Distance, VectorParams

import meow_ai_agent.model.base as base


# 这里是轻量级逻辑
# 正常商业生产逻辑一般是
#
# 首先对于数据输入（一次性或定期运行）：
# 1. 对于收集的各种文档（PDF、Word、网页、数据库等）先清洗（去重、去除噪声、PII 脱敏），然后结构化提取（表格、图片描述、元数据）
# 2. 采用语义分块（Semantic Chunking）、递归分块+重叠、或基于标题/段落的层次分，保持语义完整性同时控制 chunk 大小（中文：200–500 tokens）
# 3. 使用强中文 Embedding（bge-m3、Qwen3-Embedding 等等），结合元数据（来源、时间、类型等）生成 Embedding
# 4. 存入向量数据库（Qdrant 或 Milvus），可以使用 Hybrid Search（向量 + BM25/关键词）、元数据过滤、稀疏向量（bge-m3 的 sparse）
# 5. 额外可以使用知识图谱（GraphRAG）、父子 chunk（Parent-Document Retriever）、摘要索引、多向量索引（ColBERT）增强
# 以上做成独立的 ETL Pipeline，支持增量更新、版本控制
#
# 对于数据输出：
# 1. 是否有必要查询扩展（Query Expansion）：把用户问题改写成多个子查询（用小型 LLM 或 HyDE）
# 2. 多查询检索（Multi-Query Retriever）
# 3. Hybrid Retrieval（向量相似度 + 关键词搜索），召回较多候选（top 20-50）（元数据过滤、时间衰减等）
# 4. 重排序（Reranking）用专用 Reranker 模型（BGE-Reranker 等）对召回的 chunks 重新打分，只保留 top 3-6 个最相关的
# 5. 压缩（Context Compression），去除冗余、总结长上下文、或用 LLM 提取关键信息
# 6. 合并相似 chunks，避免 token 浪费
# 7. 构建提示词，比如明确指示 LLM：“只基于以下上下文回答，如果不确定就说不知道”
# 8. 可加入 Self-Check / Guardrails（生成后验证是否 grounded）
# 9. 流式（Streaming）输出
#
# 额外的：
# 1. 引用来源（Citation）
# 2. 幻觉检测、事实一致性检查
# 3. 安全过滤（有害内容阻断）

# ==================== 文档加载 ====================

def load_docs():
    docs = []
    for file in os.listdir("data/docs"):
        with open(f"data/docs/{file}", "r", encoding="utf-8") as f:
            docs.append({
                "text": f.read(),
                "source": file
            })
    return docs


# ==================== 文档切分 ====================

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=200
)


def split_docs(docs):
    chunks = []
    for doc in docs:
        splits = splitter.split_text(doc["text"])
        for i, s in enumerate(splits):
            chunks.append(
                Document(
                    page_content=s,
                    metadata={
                        "source": doc["source"],
                        "chunk_id": i
                    }
                )
            )
    return chunks


# ==================== 向量库 ====================

knowledge_base = "knowledge_base"

# 临时测试，每次清空
if base.qdrant_cli.collection_exists(knowledge_base):
    base.qdrant_cli.delete_collection(knowledge_base)

# 知识库
if not base.qdrant_cli.collection_exists(knowledge_base):
    base.qdrant_cli.create_collection(
        collection_name=knowledge_base,
        vectors_config=VectorParams(
            size=1024,
            distance=Distance.COSINE
        )
    )

vectorstore_knowledge_base = QdrantVectorStore(
    client=base.qdrant_cli,
    collection_name=knowledge_base,
    embedding=base.emb
)

# ==================== 检索器 ====================

retriever_knowledge_base = vectorstore_knowledge_base.as_retriever(
    search_kwargs={
        "k": 5
    }
)

# ==================== 添加文档 ====================

vectorstore_knowledge_base.add_documents(split_docs(load_docs()))

# ==================== 模型配置 ====================


system_prompt_rag = """
你是一个严谨的AI助手，只能基于提供的上下文回答。

如果答案不在上下文中，请回答：不知道。

上下文内容：

{context_text}

"""
prompt_rag = ChatPromptTemplate.from_messages([("system", system_prompt_rag), ("placeholder", "{messages}"), ])


# ==================== 节点定义 ====================


def intent_rag_node(state: base.AgentState):
    logger.info("Intent rag node")
    query = state["messages"][-1].content

    # 检索
    ret_docs = retriever_knowledge_base.invoke(query)
    context_text = "\n\n".join([doc.page_content for doc in ret_docs])

    # 消息
    messages = prompt_rag.format_messages(
        context_text=context_text,
        messages=state["messages"]
    )

    response = base.llm.invoke(messages)
    return {"messages": [response]}
