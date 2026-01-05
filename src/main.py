from src.graph import build_graph
from src.state import GraphState

from langchain_groq.chat_models import ChatGroq
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Initialize LangChain Groq chat model wrapper
groq_llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0.2)


def main():
    
    # Build the graph
    graph = build_graph(groq_llm)

    # Create initial state
    initial_state: GraphState = {
        "user_query": "Should a B2B SaaS startup enter the healthcare AI market in 2025?",
        "plan": [],
        "current_task": "",
        "research_results": {},
        "quality_flags": {},
        "final_report": None,
        "confidence_score": None,
        "metadata": {}
    }

    # Invoke the graph
    final_state = graph.invoke(initial_state)

    # Print result
    print("\n== QUALITY FLAGS ==")
    for task, flag in final_state["quality_flags"].items():
        print(f"- {task}: {flag}")

    print("\n== FINAL REPORT ==")
    print(final_state["final_report"])

    print("\n== CONFIDENCE SCORE ==")
    print(final_state["confidence_score"])


if __name__ == "__main__":
    main()