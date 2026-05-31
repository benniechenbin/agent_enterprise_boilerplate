from langchain_core.runnables import RunnableConfig
from app.schemas.state import GraphState
from app.core.container import container
from loguru import logger

def planner_node(state: GraphState, config: RunnableConfig) -> dict:
    """
    规划节点：将任务拆解为具体的执行步骤。
    """
    logger.info("进入规划节点 (Planner Node)")
    
    # 优先从 config 获取注入的 LLM
    llm = config.get("configurable", {}).get("llm_service")
    if not llm:
        llm = container.get_llm()
    
    # 此处为演示逻辑
    return {
        "messages": [("assistant", "规划：第一步是调研该主题。")],
        "next_step": "executor",
        "is_finished": False
    }
