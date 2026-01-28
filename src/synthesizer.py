from __future__ import annotations

from typing import List
from src.state import GraphState, ResearchItem

import time
from src.observability.metrics import AGENT_ERRORS, AGENT_LATENCY


def _flatten_approved_findings(state: GraphState) -> List[tuple[str, ResearchItem]]:
    approved = []
    for task, findings in state["research_results"].items():
        if state["quality_flags"].get(task) != "approved":
            continue
        for item in findings:
            approved.append((task, item))
    return approved


def synthesizer_node(state: GraphState, llm) -> GraphState:
    # Add timing
    start_time = time.time()

    approved = _flatten_approved_findings(state)

    if not approved:
        state["final_report"] = "No approved research findings were available to synthesize."
        state["confidence_score"] = 0.0
        return state

    bullets = []
    confidences = []
    for task, item in approved:
        bullets.append(f"- Task: {task}\n  Finding: {item['summary']}\n  Evidence: {item['evidence']}\n  Confidence: {item['confidence']}")
        confidences.append(float(item["confidence"]))

    avg_conf = sum(confidences) / len(confidences)

    prompt = (
        "You are a decision-ready research synthesizer.\n"
        "Use ONLY the approved findings below.\n"
        "Write a report with:\n"
        "1) Executive Summary\n"
        "2) Evidence-backed analysis (group by themes)\n"
        "3) Risks and unknowns\n"
        "4) Final recommendation: Go / No-Go / Conditional Go\n"
        "Keep it concise and actionable.\n\n"
        "APPROVED FINDINGS:\n"
        + "\n\n".join(bullets)
    )

    report = llm.invoke(prompt).content

    state["final_report"] = report
    state["confidence_score"] = round(avg_conf, 3)

    try:
        # synthesizer logic
        return state
    except Exception as e:
        AGENT_ERRORS.labels(agent_name="synthesizer").inc()
        raise e
    finally:
        elapsed_ms = (time.time() - start_time) * 1000
        AGENT_LATENCY.labels(agent_name="synthesizer").observe(elapsed_ms)
