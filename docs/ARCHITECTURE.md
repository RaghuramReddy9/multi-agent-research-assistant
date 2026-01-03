# Multi-Agent Architecture — Decision-Ready Research Assistant

## Overview

This system is a **multi-agent, graph-orchestrated research assistant** designed to convert vague, high-level questions into **structured, evidence-backed, decision-ready reports**.

The architecture follows a **Planner → Workers → Critic → Synthesizer** pattern and is orchestrated using **LangGraph** to ensure stateful, traceable, and deterministic execution.

This design mirrors real-world agent systems used in enterprise AI teams.

---

## Shared State (Single Source of Truth)

All agents communicate **only through shared state**.  
No agent directly calls another agent.

### Core State Fields

```text
user_query: str
plan: list[str]

research_results: {
  <task_name>: [
    {
      summary: str,
      evidence: list[str],
      confidence: float
    }
  ]
}

quality_flags: {
  <task_name>: str   # e.g. "ok", "weak_sources", "needs_retry"
}

final_report: str
confidence_score: float

metadata: {
  token_usage: dict,
  latency_ms: dict,
  retries: int
}
```
### Why this matters

- Enables deterministic execution

- Makes retries safe and debuggable

- Supports observability and evaluation

---

## Multi-Agent Roles & Responsibilities

This system is built using a **multi-agent architecture** where each agent has a clear, single responsibility.
Agents do **not** communicate directly with each other. All coordination happens through shared state and graph-based routing.

---

## 1. Planner Agent

### Purpose
Convert an ambiguous, high-level user question into a **structured and actionable research plan**.

### Responsibilities
- Analyze the user’s research question
- Identify key research dimensions (market, technical, risk, etc.)
- Break the problem into ordered, independent research tasks
- Define expectations for downstream agents

### Input
- `user_query`

### Output
```json
{
  "plan": [
    "Market size and growth",
    "Competitive landscape",
    "Regulatory and compliance risks",
    "Technical feasibility"
  ]
}
```
### Why This Agent Matters

- Separates reasoning from execution
- Enables parallel research
- Makes system behavior explainable and auditable

---

## 2. Research Agents (Parallel Workers)

Each research agent executes one task from the plan and produces factual, evidence-backed results.

### Examples

- MarketResearchAgent
- TechnicalResearchAgent
- RiskAndComplianceAgent

### Responsibilities

- Execute an assigned research task
- Use tools (web search, RAG, documents) to gather facts
- Summarize findings in a structured format
- Assign a confidence score to results

### Input

- One task from `plan`

### Output
```json
{
  "summary": "Healthcare AI market growing at ~25% CAGR",
  "evidence": ["source_1", "source_2"],
  "confidence": 0.72
}
```
### Rules

- No opinions
- No final recommendations
- Facts, evidence, and confidence only

---

## 3. Critic / Verifier Agent

### Purpose
Act as a quality control gate before synthesis.

### Responsibilities
- Review outputs from all research agents
- Detect hallucinations or unsupported claims
- Flag weak or insufficient evidence
- Decide whether specific tasks must be re-run

### Input
- `research_results`

### Output
```jason
{
  "status": "needs_retry",
  "reason": "Insufficient regulatory sources"
}
```

### Why This Agent Matters
- Prevents weak data from influencing decisions
- Makes evaluation explicit rather than implicit
- Reflects production-grade AI validation practices

---

## 4. Synthesizer Agent

## Purpose
Transform validated research into a decision-ready report for real-world use.

## Responsibilities
- Aggregate validated research findings
- Compare tradeoffs across domains
- Explicitly surface risks, assumptions, and unknowns
- Produce a clear, actionable recommendation

## Input
- Validated `research_results`

## Output
- `final_report`
- `confidence_score`

## Report Structure
- Executive Summary
- Evidence-backed analysis
- Risks and unknowns
- Final recommendation:
    - Go / No-Go / Conditional Go

---

## Execution Logic
1. Planner Agent generates a structured research plan
2. Research Agents execute tasks in parallel
3. Critic Agent validates research quality
4. Failed tasks are retried if needed
5. Synthesizer Agent produces the final report

All execution order, retries, and state transitions are controlled by LangGraph, ensuring deterministic and reproducible runs.

---

## Key Design Principles
- Single-responsibility agents
- Shared state as the source of truth
- Explicit handoffs and quality gates
- Extendable to monitoring, cost tracking, and observability