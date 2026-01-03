from src.graph import build_graph
from src.state import GraphState

from dotenv import load_dotenv
from langchain_groq.chat_models import ChatGroq

# Load environment variables from .env file
load_dotenv()

# Initialize LangChain Groq chat model wrapper
groq_llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.2)


def main():
    
    # Build the graph
    graph = build_graph(groq_llm)

    # Create initial state
    initial_state: GraphState = {
        "user_query": "Should a B2B SaaS startup enter the healthcare AI market in 2025?",
        "plan": [],
        "research_results": {},
        "quality_flags": {},
        "final_report": None,
        "confidence_score": None,
        "metadata": {}
    }

    # Invoke the graph
    final_state = graph.invoke(initial_state)

    # Print result
    print("\n=== GENERATED RESEARCH PLAN ===")
    for idx, task in enumerate(final_state["plan"], start=1):
        print(f"{idx}. {task}")


if __name__ == "__main__":
    main()
