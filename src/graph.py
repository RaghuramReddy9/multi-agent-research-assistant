from langgraph.graph import StateGraph, END

from src.state import GraphState
from src.planner import planner_node


def build_graph(llm):
    """
    Builds and returns the LangGraph for the research assistant.
    Currently includes only the Planner node.
    """
    # Create a stateful graph with GraphState
    graph = StateGraph(GraphState)

    # Register nodes
    graph.add_node("planner", lambda state: planner_node(state, llm))

    # Define entry point
    graph.set_entry_point("planner")

    # Define exit point
    graph.add_edge("planner", END)

    # Compile the graph
    return graph.compile()