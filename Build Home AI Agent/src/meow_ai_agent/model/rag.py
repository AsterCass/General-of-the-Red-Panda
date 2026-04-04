import os

import jieba
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    Docx2txtLoader
)
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_qdrant import QdrantVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from loguru import logger
from qdrant_client.models import Distance, VectorParams
from rank_bm25 import BM25Okapi

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
# 6. 合并相似 chunks，避免计算量浪费（需要先于 reranking ）
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
        path = os.path.join("data/docs", file)

        try:
            if file.endswith((".txt", ".md")):
                loader = TextLoader(path, encoding="utf-8")

            elif file.endswith(".pdf"):
                loader = PyPDFLoader(path)

            elif file.endswith(".docx"):
                loader = Docx2txtLoader(path)

            else:
                continue

            docs.extend(loader.load())

        except Exception as e:
            logger.error(f"{file} Parse failed: {e}")

    return docs


# ==================== 文档切分 ====================

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=200
)


def split_docs(docs):
    chunks = []
    for doc in docs:
        splits = splitter.split_text(doc.page_content)
        for i, s in enumerate(splits):
            chunks.append(
                Document(
                    page_content=s,
                    # todo 这里可以丰富metadata的细节，然后查询的时候利用轻量的筛选（这里还是老三层，字符串+Embedding+轻量LLM兜底），
                    #  并利用 from qdrant_client.models import Filter 写入 retriever 在向量搜索前加一层过滤
                    metadata={
                        "source": doc.metadata.get("source", "unknown"),
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
        "k": 5,
        # match=MatchValue(value="xxx.md")
    }
)

# ==================== 添加文档 ====================

# 文档
documents = split_docs(load_docs())

# BM25
tokenized_corpus = [
    jieba.lcut(doc.page_content)
    for doc in documents
]

bm25 = BM25Okapi(tokenized_corpus)

# Embedding
vectorstore_knowledge_base.add_documents(documents)

# ==================== 模型配置 ====================


system_prompt_rag = """
你是一个严谨的AI助手，只能基于提供的上下文回答。

如果答案不在上下文中，请回答：不知道。

上下文内容：

{context_text}

"""
prompt_rag = ChatPromptTemplate.from_messages([("system", system_prompt_rag), ("placeholder", "{messages}"), ])


# ==================== 额外方法 ====================

def bm25_search(query, top_k=10):
    tokenized_query = jieba.lcut(query)

    scores = bm25.get_scores(tokenized_query)

    top_k_idx = sorted(
        range(len(scores)),
        key=lambda i: scores[i],
        reverse=True
    )[:top_k]

    return [documents[i] for i in top_k_idx]


def merge_docs(vec_docs, bm25_docs):
    seen = set()
    results = []

    for d in vec_docs + bm25_docs:
        key = d.page_content
        if key not in seen:
            seen.add(key)
            results.append(d)

    return results

# ==================== 节点定义 ====================


def intent_rag_node(state: base.AgentState):
    logger.info("Intent rag node")
    query = state["messages"][-1].content
    # todo 这里可以对于本身 query 进行优化/拆分/扩展等等，同样是需要使用老三层（字符串+Embedding+轻量LLM）

    # todo 检索
    #  可以对于 query 提取 metadata 过滤查询，同样是需要使用老三层（字符串+Embedding+轻量LLM）进行打标签
    ret_docs_vec = retriever_knowledge_base.invoke(query)
    # bm25
    ret_docs_bm25 = bm25_search(query, top_k=5)
    logger.info(f"Results: {len(ret_docs_vec)}")
    logger.info(f"Results: {len(ret_docs_bm25)}")
    # 去重
    ret_docs = merge_docs(ret_docs_vec, ret_docs_bm25)
    logger.info(f"Results: {len(ret_docs)}")
    # todo 这里可以加入 reranker（Qdrant 中的检索本质上还是向量匹配，即 embedding cosine 向量余弦比较，
    #  一般对于 reranker 是语义匹配（cross attention），所以在查询阶段而言，向量匹配不需要模型，而 reranker 是需要专门模型的）
    context_text = "\n\n".join([doc.page_content for doc in ret_docs])

    # 消息
    messages = prompt_rag.format_messages(
        context_text=context_text,
        messages=state["messages"]
    )

    response = base.llm.invoke(messages)
    return {"messages": [response]}
