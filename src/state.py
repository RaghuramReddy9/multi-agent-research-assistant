from typing import TypedDict, List, Dict, Any, Optional


class ResearchItem(TypedDict):
    summary: str
    evidence: List[str]
    confidence: float


class GraphState(TypedDict):
    # original user input
    user_query: str

    # planer output
    plan: List[str]

    # Research results keyed by task name
    research_results: Dict[str, List[ResearchItem]]

    # Quality flags set by a critic agent
    quality_flags: Dict[str, str]

    # final output produced by the Synthesizer
    final_report: Optional[str]
    confidence_score: Optional[float]

    # system metadata (cost, retries, timing)
    metadata: Dict[str, Any]