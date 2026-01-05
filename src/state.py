from typing import TypedDict, List, Dict, Any, Optional


class ResearchItem(TypedDict):
    summary: str
    evidence: List[str]
    confidence: float


class GraphState(TypedDict):
    """
    GraphState is the single source of truth for the system.
    All agents must read/write exclusively through this state.
    This enables deterministic execution, retries, and observability.
    """
    # original user input
    user_query: str

    # planer output
    plan: List[str]

    # Which task is currently in process
    current_task: str

    # Research results keyed by task name
    research_results: Dict[str, List[ResearchItem]]

    # Quality flags set by a critic agent
    quality_flags: Dict[str, str]

    # final output produced by the Synthesizer
    final_report: Optional[str]
    confidence_score: Optional[float]

    # system metadata (cost, retries, timing)
    metadata: Dict[str, Any]