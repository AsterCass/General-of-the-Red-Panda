from pathlib import Path

from langchain.tools import tool
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from loguru import logger

def ingest(doc_path: Path, index_path: Path):
    if not index_path.exists() or (not index_path.exists()):
        return
    documents = SimpleDirectoryReader(doc_path).load_data()
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist(persist_dir=index_path)
    logger.info("Ingest Complete")

@tool
def query_docs(question: str) -> str:
    """查询本地知识库（PDF/TXT）"""
    storage_context = StorageContext.from_defaults(persist_dir="./rag/index")
    index = load_index_from_storage(storage_context)
    query_engine = index.as_query_engine()
    response = query_engine.query(question)
    return str(response)
