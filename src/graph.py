from langgraph.graph import StateGraph, END

from src.state import GraphState
from src.planner import planner_node
from src.tasks import task_dispatcher_node
from src.research import research_node
from src.critic import critic_node
from src.synthesizer import synthesizer_node


def build_graph(llm):
    
    # Create a stateful graph with GraphState
    graph = StateGraph(GraphState)

    # Register nodes
    graph.add_node("planner", lambda state: planner_node(state, llm))
    graph.add_node("dispatch", task_dispatcher_node)
    graph.add_node("research", lambda s: research_node(s, llm))
    graph.add_node("critic", critic_node)
    graph.add_node("synthesizer", lambda s: synthesizer_node(s, llm))

    # Define entry point
    graph.set_entry_point("planner")

    graph.add_edge("planner", "dispatch")
    graph.add_edge("dispatch", "research")
    graph.add_edge("research", "critic")


    def route_after_critic(state: GraphState) -> str:
        # If no more tasks left, end. Otherwise loop.
        if not state["plan"]:
            return "synthesizer"
        return "dispatch"

    graph.add_conditional_edges(
        "critic",
        route_after_critic,
        {
            "dispatch": "dispatch",
            "synthesizer": "synthesizer",
        }
    )

    graph.add_edge("synthesizer", END)

    return graph.compile()