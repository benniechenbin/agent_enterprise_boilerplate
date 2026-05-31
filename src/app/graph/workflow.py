from langgraph.graph import StateGraph, END
from app.schemas.state import GraphState
from app.nodes.planner import planner_node
from app.nodes.executor import executor_node
from app.multi_agent_lab.scout import scout_node

def create_workflow(strategy: str = "default"):
    """
    工作流工厂：根据策略动态组装 Graph。
    """
    workflow = StateGraph(GraphState)

    if strategy == "lab":
        # 实验室模式：包含侦察兵节点
        workflow.add_node("scout", scout_node)
        workflow.add_node("planner", planner_node)
        workflow.add_node("executor", executor_node)

        workflow.set_entry_point("scout")
        workflow.add_edge("scout", "planner")
        workflow.add_edge("planner", "executor")
        workflow.add_edge("executor", END)
    else:
        # 默认模式
        workflow.add_node("planner", planner_node)
        workflow.add_node("executor", executor_node)

        workflow.set_entry_point("planner")
        workflow.add_edge("planner", "executor")
        workflow.add_edge("executor", END)

    return workflow.compile()

# 导出默认工作流实例（兼容旧逻辑）
app_workflow = create_workflow()
