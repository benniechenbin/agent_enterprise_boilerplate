from langgraph.graph import StateGraph, END
from app.schemas.state import GraphState
from app.nodes.planner import planner_node
from app.nodes.executor import executor_node

def create_workflow():
    """
    编译 LangGraph 工作流。
    """
    workflow = StateGraph(GraphState)

    # 添加节点
    workflow.add_node("planner", planner_node)
    workflow.add_node("executor", executor_node)

    # 定义边（节点间的流转）
    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "executor")

    # 条件判断边或直接结束
    def should_continue(state: GraphState):
        if state.get("is_finished"):
            return END
        return "planner" # 或其他逻辑

    workflow.add_edge("executor", END)

    return workflow.compile()

app_workflow = create_workflow()
