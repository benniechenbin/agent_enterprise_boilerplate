from langchain_core.runnables import RunnableConfig
from app.schemas.state import GraphState
from app.core.container import container
from loguru import logger

def executor_node(state: GraphState, config: RunnableConfig) -> dict:
    """
    执行节点：执行规划好的具体步骤。
    """
    logger.info("进入执行节点 (Executor Node)")
    
    # 优先从 config 获取注入的 LLM
    llm = config.get("configurable", {}).get("llm_service")
    if not llm:
        llm = container.get_llm()

    # 此处为演示逻辑
    return {
        "messages": [("assistant", "执行：第一步执行完毕。")],
        "next_step": "end",
        "is_finished": True
    }
