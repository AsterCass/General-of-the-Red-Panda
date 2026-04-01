# from langchain.tools import tool
# from duckduckgo_search import DDGS
#
# @tool
# def web_search(query: str) -> str:
#     with DDGS() as ddgs:
#         results = ddgs.text(query, max_results=3)
#         return "\n".join([r["body"] for r in results])