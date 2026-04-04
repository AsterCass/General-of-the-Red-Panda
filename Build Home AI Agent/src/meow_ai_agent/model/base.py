from typing import TypedDict, Annotated, Optional

from langchain_core.messages import AIMessage
from langchain_ollama import ChatOllama
from langchain_ollama import OllamaEmbeddings
from langchain_qdrant import QdrantVectorStore
from langgraph.graph.message import add_messages
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

import meow_ai_agent.constants.env as env
from meow_ai_agent.constants.enums import IntentStatus


# ==================== 节点状态 ====================

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]  # 自动合并消息历史
    intent: IntentStatus | None  # 意图相关（目前单次对话确定意图后，不再会更改，方便测试子功能）
    intent_force: Optional[bool] | None  # 是否为强行进入意图
    pending_action: Optional[AIMessage] | None  # 工具相关
    confirmed: Optional[bool] | None  # 工具相关


# ==================== 模型 ====================

llm = ChatOllama(
    model=env.MODEL_NAME,
    base_url=env.OLLAMA_BASE_URL,
)

emb = OllamaEmbeddings(
    model=env.EMBED_TEXT_MODEL_NAME,
    base_url=env.OLLAMA_BASE_URL,
)

llm_l = ChatOllama(
    model=env.MODEL_NAME_LIGHT,
    base_url=env.OLLAMA_BASE_URL,
    temperature=0
)

# ==================== 向量库 ====================

qdrant_cli = QdrantClient(
    url=env.QDRANT_URL
)

intent_router = "intent_router"

# 临时测试，每次清空
if qdrant_cli.collection_exists(intent_router):
    qdrant_cli.delete_collection(intent_router)

# 意图库
if not qdrant_cli.collection_exists(intent_router):
    qdrant_cli.create_collection(
        collection_name=intent_router,
        vectors_config=VectorParams(
            size=1024,
            distance=Distance.COSINE
        )
    )

vectorstore_intent_router = QdrantVectorStore(
    client=qdrant_cli,
    collection_name=intent_router,
    embedding=emb
)

# ==================== 检索器 ====================

# retriever_knowledge_base = vectorstore_knowledge_base.as_retriever(
#     search_kwargs={
#         "k": 3
#     }
# )
#
# retriever_intent_router = vectorstore_intent_router.as_retriever(
#     search_kwargs={
#         "k": 3
#     }
# )
