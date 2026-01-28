from src.state import GraphState

import time
from src.observability.metrics import AGENT_ERRORS, AGENT_LATENCY


MIN_CONFIDENCE_THRESHOLD = 0.85


def critic_node(state: GraphState) -> GraphState:
    """
    Critic node:
    - Evaluates research quality for a single task
    - Decides whether results are acceptable or need retry
    """
    # Initialize timing
    start_time = time.time()

    results = state["research_results"]
    flags = state["quality_flags"]

    for task, findings in results.items():
        if not findings:
            flags[task] = "empty_research"

    task = state["current_task"].strip()
    if not task:
        return state

    findings = state["research_results"].get(task, [])

    if not findings:
        state["quality_flags"][task] = "needs_retry"
        return state

    # Count high-confidence findings
    high_confidence_count = sum(
        1 for item in findings if item["confidence"] >= MIN_CONFIDENCE_THRESHOLD
    )

    # Simple acceptance rule (can evolve later)
    if high_confidence_count >= 2:
        state["quality_flags"][task] = "approved"
    else:
        state["quality_flags"][task] = "needs_retry"

    try:
        # critic logic
        return state
    
    except Exception as e:
        AGENT_ERRORS.labels(agent_name="critic").inc()
        raise e
    
    finally:
        elapsed_ms = (time.time() - start_time) * 1000
        AGENT_LATENCY.labels(agent_name="critic").observe(elapsed_ms)
