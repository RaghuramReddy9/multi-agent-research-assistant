# Metrics Reference

## 1. Overview
## 2. Core Metrics
## 3. Supporting Metrics
## 4. Metric Usage Guidelines

---

## 1. Overview

This document defines the core observability metrics emitted by the AI application.
Each metric is designed to capture a specific aspect of system behavior, including performance, usage, and reliability.
These metrics are used to power dashboards, alerts, and operational decision-making.
Clear definitions ensure consistent interpretation across monitoring and on-call workflows.

---

## 2. Core Metrics

### 2.1 Request Latency

| Metric Type | Description |
|------------|-------------|
| Histogram  | Measures end-to-end request processing time from receipt to response. |

**Why it matters:**  
Latency directly impacts user experience and is often the first indicator of upstream model or infrastructure degradation.

**Healthy behavior:**  
Latency remains stable with predictable variation as traffic changes.

**Unhealthy signals:**  
Sustained increases in high-percentile latency or sudden spikes without corresponding traffic growth.


### 2.2 Token Usage

| Metric Type | Description |
|------------|-------------|
| Counter    | Tracks the total number of tokens consumed during LLM inference. |

**Why it matters:**  
Token usage directly correlates with inference cost and can indicate inefficient prompts or routing logic.

**Healthy behavior:**  
Token usage grows proportionally with traffic and remains stable for similar request types.

**Unhealthy signals:**  
Sudden increases in token consumption without a corresponding increase in traffic, often indicating prompt regressions or misuse.

### 2.3 Error Rate

| Metric Type | Description |
|------------|-------------|
| Counter    | Counts failed requests due to application or upstream LLM errors. |

**Why it matters:**  
Error rates reflect system reliability and directly impact user trust and downstream workflows.

**Healthy behavior:**  
Errors remain rare and isolated, with no sustained upward trends.

**Unhealthy signals:**  
Repeated failures, sustained error spikes, or correlated increases alongside latency degradation.

---

## 3. Supporting Metrics

Supporting metrics provide additional context during investigations but are not used as primary alert signals.
These metrics help explain changes observed in core metrics such as latency, token usage, or error rates.

Examples include request volume, request distribution by route or agent, and retry counts.
While valuable for debugging and analysis, supporting metrics are typically evaluated alongside core metrics rather than independently.
This approach helps prevent alert fatigue and keeps operational focus on user-impacting issues.

---

## 4. Metric Usage Guidelines

Metrics should be interpreted as trends rather than isolated data points.
Single spikes may occur due to transient conditions and do not always indicate systemic issues.
Operational decisions should consider correlations between latency, token usage, and error rates.

Alerts should be configured conservatively and reviewed periodically to ensure they remain meaningful.
Changes to prompts, routing logic, or model configuration should always be evaluated for their impact on existing metrics.
Consistent metric interpretation is essential for maintaining reliable and cost-effective AI systems.
