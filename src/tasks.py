from src.state import GraphState


def task_dispatcher_node(state: GraphState) -> GraphState:
    """
    Pops the next task from the plan and sets it as current_task.
    """
    if not state["plan"]:
        state["current_task"] = ""
        return state
    
    task = state["plan"].pop(0)
    state["current_task"] = task
    return state

    