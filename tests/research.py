from src.research import research_node
from src.state import GraphState
from dotenv import load_dotenv
from langchain_groq.chat_models import ChatGroq

# Load environment variables from .env file
load_dotenv()

# Initialize LangChain Groq chat model wrapper
groq_llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0.2)

def main():
    # Initialize LLM 
    llm = groq_llm

    # Create initial state
    state: GraphState = {
        "user_query": "Test Research Agent",
        "plan": [],
        "research_results": {},
        "quality_flags": {},
        "final_report": None,
        "confidence_score": None,
        "metadata": {}
    }

    # define one research task
    task = "Analyze the regulatory landscape for AI in healthcare in the US and EU."

    # run research Agent
    updated_state = research_node(state, task, llm)

    # print research results
    print("\n=== RESEARCH RESULTS ===")
    for item in updated_state["research_results"][task]:
        print(f"- Summary: {item['summary']}")
        print(f"  Evidence: {item['evidence']}")
        print(f"  Confidence: {item['confidence']}\n")

if __name__ == "__main__":
    main()
