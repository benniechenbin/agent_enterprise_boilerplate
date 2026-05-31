from typing import Annotated, TypedDict, List
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class GraphState(TypedDict):
    """
    LangGraph 工作流的核心状态定义。
    """
    messages: Annotated[List[BaseMessage], add_messages]
    next_step: str
    is_finished: bool
