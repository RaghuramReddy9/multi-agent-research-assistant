from src.graph import build_graph
from src.state import GraphState

from langchain_groq.chat_models import ChatGroq
from dotenv import load_dotenv

import time
import uuid

from src.observability.metrics import (
    REQUESTS_TOTAL,
    REQUESTS_SUCCESS,
    REQUESTS_FAILURE,
    REQUEST_LATENCY,
)

from prometheus_client import start_http_server



# Load environment variables from .env file
load_dotenv()

# Initialize LangChain Groq chat model wrapper
groq_llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.2)


def main():

    # Start request metrics
    request_id = str(uuid.uuid4())
    REQUESTS_TOTAL.inc()
    start_time = time.time()
    
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

    try:
        # Invoke the graph
        final_state = graph.invoke(initial_state)
        REQUESTS_SUCCESS.inc()

    except Exception as e:
        REQUESTS_FAILURE.inc()
        raise e
    
    finally:
        elapsed_ms = (time.time() - start_time) * 1000
        REQUEST_LATENCY.observe(elapsed_ms)

    # # Print result (unchanged)
    # print("\n== QUALITY FLAGS ==")
    # for task, flag in final_state["quality_flags"].items():
    #     print(f"- {task}: {flag}")

    # print("\n== FINAL REPORT ==")
    # print(final_state["final_report"])

    # print("\n== CONFIDENCE SCORE ==")
    # print(final_state["confidence_score"])

    # Keep the metrics server running
    input("\nMetrics server running on http://localhost:8000/metrics\nPress Enter to exit...")



if __name__ == "__main__":
    # Start Prometheus metrics server
    start_http_server(8000)

    main()