# Multi-Agent Decision-Ready Research Assistant

A **LangGraph-orchestrated multi-agent system** that converts vague, high-level questions into **structured, evidence-backed, decision-ready reports**.

This project demonstrates how real-world enterprise AI teams design agentic systems with **explicit planning, execution, validation, and synthesis stages**, rather than monolithic chatbots.

---

## What This System Does

Given a complex research question, the system:

1. Breaks the question into structured research tasks
2. Executes each task via specialized research agents
3. Validates research quality through an explicit critic gate
4. Synthesizes approved findings into a **final decision-ready report**
5. Outputs a **confidence score** reflecting research reliability

The result is a deterministic, auditable workflow suitable for business and strategic decision-making.

---

## Architecture Overview
Planner → Task Dispatcher → Research Agents → Critic → Synthesizer → Final Report

---


### Key Design Principles

- **Single source of truth** via shared state (`GraphState`)
- **No direct agent-to-agent communication**
- **Explicit quality gates** before synthesis
- **Deterministic execution** using LangGraph
- **Extendable** to retries, observability, and evaluation

This mirrors production-grade agent systems used in enterprise AI teams.

---

## Agent Responsibilities

### Planner Agent
- Converts an ambiguous user query into a structured research plan
- Identifies independent research dimensions (market, risk, regulation, etc.)

### Task Dispatcher
- Assigns one research task at a time to worker agents
- Controls execution order deterministically

### Research Agents
- Execute individual research tasks
- Produce structured outputs:
  - Summary
  - Evidence sources
  - Confidence score
- No opinions or recommendations

### Critic Agent
- Evaluates research quality and confidence
- Flags weak or insufficient findings
- Acts as a quality gate before synthesis

### Synthesizer Agent
- Aggregates only **approved** research findings
- Produces a structured, decision-ready report
- Outputs an overall confidence score

---

## Shared State Contract

All agents read from and write to a shared state object:

```text
user_query: str
plan: list[str]

research_results:
  <task>: [
    { summary, evidence, confidence }
  ]

quality_flags:
  <task>: approved | needs_retry | empty_research

final_report: str
confidence_score: float

metadata:
  token_usage
  latency_ms
  retries
```
This design enables safe retries, observability, and evaluation.

---

## Tech Stack

- Python
- LangGraph (agent orchestration)
- LangChain
- Groq LLM `(gpt-oss-120b)` 
- Typed shared state for deterministic execution

--

## How to Run
```python 
python -m src.main
```
After execution, the system prints:
- Quality flags per task
- Final synthesized report
- Overall confidence score

---

## Why This Matters

Most AI demos stop at chatbots.

This project demonstrates:
- Real agent orchestration
- Explicit reasoning vs execution separation
- Quality validation before decisions
- Production-ready system thinking

It is designed as a foundation for:
- LLM observability
- Evaluation pipelines
- Cost and latency monitoring
- Enterprise AI workflows

--- 

## Author

**Raghuramreddy Thirumalareddy**

Aspiring Generative AI Engineer focused on building **production-grade GenAI systems** 

🔗 LinkedIn: https://www.linkedin.com/in/raghuramreddy-ai


