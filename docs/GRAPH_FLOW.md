# LangGraph Execution Flow — Multi-Agent Research Assistant

This document defines the **graph-based execution flow** for the Decision-Ready Research Assistant.
The system is orchestrated using **LangGraph**, where each agent is represented as a node and execution is controlled through explicit edges and conditional routing.

This design ensures **deterministic, debuggable, and production-grade execution**.

---

## 1. Graph Nodes

Each agent in the system is implemented as a **LangGraph node**.

| Node Name | Agent Role | Responsibility |
|---------|-----------|----------------|
| `planner_node` | Planner Agent | Decomposes the user query into structured research tasks |
| `research_node` | Research Agents | Executes research tasks in parallel |
| `critic_node` | Critic / Verifier Agent | Validates research quality and detects weak evidence |
| `synthesizer_node` | Synthesizer Agent | Produces the final decision-ready report |
| `END` | Terminal | Marks completion of execution |

---

## 2. Graph Entry Point

`START → planner_node`

The Planner Agent is always the entry point because:
- Planning must occur exactly once
- All downstream execution depends on the generated plan

---

## 3. Planner → Research (Fan-Out Execution)

After planning:
`planner_node → research_node`

Execution behavior:
- The Planner Agent writes an ordered `plan[]` into shared state
- LangGraph spawns **parallel executions** of Research Agents
- Each Research Agent processes exactly one task from the plan

This enables scalable and efficient parallel research.

---

## 4. Research → Critic (Quality Gate)

Once all research tasks complete:
`research_node → critic_node`

At this stage:
- All research outputs are available in shared state
- No synthesis is allowed before validation
- Quality control is enforced explicitly

---

## 5. Conditional Routing (Retry vs Continue)

The Critic Agent evaluates research quality and emits one of two outcomes.

### Critic Output — Approved
```json
{
  "status": "approved"
}
```
`Critic Output — Needs Retry`
```json
{
  "status": "needs_retry",
  "failed_tasks": ["Regulatory and compliance risks"]
}
```

---

## 6. Conditional Edges

Based on the Critic’s decision:
```lua
critic_node
 ├─ if status == "approved" → synthesizer_node
 └─ if status == "needs_retry" → research_node (failed tasks only)
```
### Key properties:
- Only failed tasks are retried
- Successful research is preserved
- Full system restart is avoided

This pattern is critical for cost-efficient, production-grade GenAI systems.

---

## 7. Synthesis and Completion

When research is approved:
```powershell
synthesizer_node → END
```
### The Synthesizer Agent:
- Aggregates validated research
- Produces the final report
- Assigns a confidence score

Execution terminates cleanly.

---

## 8. Full Execution Flow (ASCII Diagram)
```sql
START
  |
  v
Planner Agent
  |
  v
Research Agents (parallel)
  |
  v
Critic Agent
  |
  +--[needs_retry]--> Research Agents (failed tasks only)
  |
  +--[approved]----> Synthesizer Agent
                        |
                        v
                       END
```

---

## 9. Why This Graph Design Is Industry-Grade
- Deterministic execution flow
- Explicit quality gates
- Partial retries instead of full restarts
- Clear separation of responsibilities
- Easily extensible to logging, monitoring, and cost tracking

This execution model mirrors how enterprise AI systems orchestrate multi-agent workflows in production.