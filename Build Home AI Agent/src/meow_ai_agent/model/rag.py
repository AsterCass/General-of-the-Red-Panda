#
# import re
# from typing import TypedDict, Annotated, Optional
#
# from langchain_core.documents import Document
# from langchain_core.messages import HumanMessage, AIMessage
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_ollama import ChatOllama
# from langchain_ollama import OllamaEmbeddings
# from langchain_qdrant import QdrantVectorStore
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langgraph.checkpoint.memory import MemorySaver
# from langgraph.constants import END
# from langgraph.graph import StateGraph
# from langgraph.graph.message import add_messages
# from langgraph.prebuilt import ToolNode
# from loguru import logger
# from qdrant_client import QdrantClient
# from qdrant_client.models import Distance, VectorParams
#
#
# import meow_ai_agent.constants.env as env
# from meow_ai_agent.utils.device import turn_off_light_bedroom, turn_off_light_living_room, close_window_living_room, \
#     turn_on_heating_bedroom, open_curtain_living_room, close_curtain_living_room
#
# # ==================== 文档切分 ====================
#
# splitter = RecursiveCharacterTextSplitter(
#     chunk_size=500,
#     chunk_overlap=100
# )
#
# # ==================== 向量库 ====================
#
# qdrant_cli = QdrantClient(
#     url=env.QDRANT_URL
# )
# collection_name = "knowledge_base"
#
# # 临时测试，每次清空
# if qdrant_cli.collection_exists(collection_name):
#     qdrant_cli.delete_collection(collection_name)
#
# if not qdrant_cli.collection_exists(collection_name):
#     qdrant_cli.create_collection(
#         collection_name=collection_name,
#         vectors_config=VectorParams(
#             size=1024,
#             distance=Distance.COSINE
#         )
#     )
#
# vectorstore = QdrantVectorStore(
#     client=qdrant_cli,
#     collection_name=collection_name,
#     embedding=emb
# )
#
# # ==================== 检索器 ====================
#
# retriever = vectorstore.as_retriever(
#     search_kwargs={
#         "k": 3
#     }
# )
#
# # ==================== 测试 ====================
#
# docs = [
#     Document(page_content="猫是哺乳动物，通常被当作宠物饲养。", metadata={"source": "wiki"}),
#     Document(page_content="狗是人类最好的朋友，常用于看家护院。", metadata={"source": "wiki"}),
#     Document(page_content="猫喜欢独处，性格相对独立。", metadata={"source": "wiki"}),
#     Document(page_content="狗通常性格忠诚，喜欢与人互动。", metadata={"source": "wiki"}),
#     Document(page_content="猫属于食肉动物，主要捕食小型动物。", metadata={"source": "wiki"}),
#     Document(page_content="狗经过人类长期驯化，是典型的家养动物。", metadata={"source": "wiki"}),
#     Document(page_content="老虎也是猫科动物，但体型巨大且危险。", metadata={"source": "wiki"}),
#     Document(page_content="狼是狗的近亲，生活在野外环境中。", metadata={"source": "wiki"}),
#     Document(page_content="猫的听觉非常敏锐，可以捕捉微小声音。", metadata={"source": "wiki"}),
#     Document(page_content="狗的嗅觉非常灵敏，常用于搜救和侦查。", metadata={"source": "wiki"}),
#     Document(page_content="猫每天会花很多时间进行自我清洁。", metadata={"source": "wiki"}),
#     Document(page_content="狗需要每天外出活动，否则容易焦虑。", metadata={"source": "wiki"}),
#     Document(page_content="猫科动物通常具有锋利的爪子和牙齿。", metadata={"source": "wiki"}),
#     Document(page_content="犬科动物通常具有群居行为。", metadata={"source": "wiki"}),
#     Document(page_content="猫的夜视能力很强，适合夜间活动。", metadata={"source": "wiki"}),
#     Document(page_content="狗可以通过训练完成复杂指令。", metadata={"source": "wiki"}),
#     Document(page_content="汽车是一种交通工具，用于人类出行。", metadata={"source": "wiki"}),
#     Document(page_content="飞机可以在空中飞行，是长途交通方式。", metadata={"source": "wiki"}),
#     Document(page_content="计算机可以执行复杂计算，是现代科技核心。", metadata={"source": "wiki"}),
#     Document(page_content="苹果是一种水果，富含维生素。", metadata={"source": "wiki"}),
# ]
#
# split_docs = splitter.split_documents(docs)
# vectorstore.add_documents(split_docs)
#
#
#
# # ret1 = retriever.invoke("猫是什么动物")
# # ret2 = retriever.invoke("什么动物嗅觉好")
# # ret3 = retriever.invoke("交通工具有哪些")
#
# # todo 这里后续可以 ret = rerank(query, ret) 使用类似 reranker = CrossEncoder("BAAI/bge-reranker-base") 模型完成
#
# # for r in ret1:
# #     print(r.page_content)
# #
# # for r in ret2:
# #     print(r.page_content)
# #
# # for r in ret3:
# #     print(r.page_content)
#
#
#
#
# def retrieve_node(state: AgentState):
#     query = state["messages"][-1].content
#     ret_doc = retriever.invoke(query)
#
#     context = "\n\n".join([d.page_content for d in ret_doc])
#
#     return {
#         "context": context
#     }
