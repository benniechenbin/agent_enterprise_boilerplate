import pytest
from app.graph.workflow import app_workflow

@pytest.mark.asyncio
async def test_workflow_execution():
    initial_state = {
        "messages": [("user", "test")],
        "next_step": "",
        "is_finished": False
    }
    
    events = []
    async for event in app_workflow.astream(initial_state):
        events.append(event)
    
    assert len(events) > 0
    # The mock workflow should at least hit planner and executor
    node_names = [list(e.keys())[0] for e in events]
    assert "planner" in node_names
    assert "executor" in node_names
