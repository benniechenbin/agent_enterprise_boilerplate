from langchain_core.tools import tool

@tool
def search_tool(query: str) -> str:
    """
    在网络上搜索信息。
    """
    # 模拟搜索结果
    return f"针对 '{query}' 的搜索结果 (已模拟)"
