from typing import TypedDict, Annotated, Optional

from langchain_core.messages import AIMessage
from langchain_ollama import ChatOllama
from langchain_ollama import OllamaEmbeddings
from langchain_qdrant import QdrantVectorStore
from langgraph.graph.message import add_messages
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from meow_ai_agent.constants.config import service_settings
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
    model=service_settings.llm_model,
    base_url=service_settings.ollama_base_url,
)

llm_ns = ChatOllama(
    model=service_settings.llm_model,
    base_url=service_settings.ollama_base_url,
    tags=["nostream"],
)

emb = OllamaEmbeddings(
    model=service_settings.embed_text_model,
    base_url=service_settings.ollama_base_url,
)

llm_l = ChatOllama(
    model=service_settings.llm_model_light,
    base_url=service_settings.ollama_base_url,
    temperature=0,
    tags=["nostream"],
)

# ==================== 向量库 ====================

qdrant_cli = QdrantClient(
    url=service_settings.qdrant_url,
)

intent_router = "intent_router"

# 指定重置时清空
if service_settings.reset_collections and qdrant_cli.collection_exists(intent_router):
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
