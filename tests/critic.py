from src.state import GraphState
from src.critic import critic_node


state: GraphState = {
    "user_query": "test",
    "plan": [],
    "research_results": {
        "Regulatory landscape": [
            {"summary": "FDA regulates SaMD", "evidence": ["fda.gov"], "confidence": 0.92},
            {"summary": "EU AI Act applies", "evidence": ["europa.eu"], "confidence": 0.88},
            {"summary": "Weak claim", "evidence": ["blog.com"], "confidence": 0.40},
        ]
    },
    "quality_flags": {},
    "final_report": None,
    "confidence_score": None,
    "metadata": {}
}

state = critic_node(state, "Regulatory landscape")

print(state["quality_flags"])
