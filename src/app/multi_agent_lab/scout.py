from langchain_core.runnables import RunnableConfig
from app.schemas.state import GraphState
from loguru import logger

def scout_node(state: GraphState, config: RunnableConfig) -> dict:
    """
    侦察兵节点 (Scout Node)：负责初步的信息搜集和环境感知。
    它是多智能体协作的“排头兵”。
    """
    logger.info("进入侦察兵节点 (Scout Node)")
    
    # 依赖注入：从 config 中获取 LLM 服务
    llm = config.get("configurable", {}).get("llm_service")
    
    if not llm:
        logger.warning("未检测到注入的 llm_service，将尝试从容器获取兜底方案")
        from app.core.container import container
        llm = container.get_llm()

    # 模拟业务逻辑
    # 实际场景下，我们会在这里调用 llm 并结合 search_tool
    last_message = state["messages"][-1].content if state["messages"] else "无初始指令"
    logger.debug(f"侦察兵收到指令: {last_message}")
    
    return {
        "messages": [("assistant", f"侦察兵报告：已完成对 '{last_message}' 的初步勘察。")],
        "next_step": "planner",
        "is_finished": False
    }
