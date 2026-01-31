# Alert Definitions

## 1. Alerting Philosophy
## 2. Latency Alert
## 3. Error Rate Alert
## 4. Token Usage Alert

---

## 1. Alerting Philosophy

Alerts are designed to signal user-impacting or cost-critical issues that require immediate attention.
They are based on sustained metric behavior rather than transient spikes.
Each alert maps directly to a documented metric and a clear operational response.
The goal is to minimize alert fatigue while maintaining system reliability.

---

## 2. Latency Alert

**Trigger Condition:**  
Sustained increase in high-percentile request latency beyond expected operating ranges.

**Why this matters:**  
Elevated latency directly impacts user experience and may indicate upstream model degradation or infrastructure constraints.

**Primary Signals:**  
- Request latency percentiles
- Correlated error rate changes

**Immediate Actions:**  
- Verify whether the issue is isolated or system-wide  
- Check recent prompt or routing changes  
- Assess upstream LLM service health

---

## 3. Error Rate Alert

**Trigger Condition:**  
Sustained increase in failed requests relative to normal baseline levels.

**Why this matters:**  
Errors represent failed user interactions and may indicate upstream outages, authentication issues, or application regressions.

**Primary Signals:**  
- Error count trends
- Correlation with latency spikes

**Immediate Actions:**  
- Identify error sources (application vs upstream)  
- Review recent deployments or configuration changes  
- Confirm whether failures are partial or complete

---

## 4. Token Usage Alert

**Trigger Condition:**  
Unexpected growth in token consumption without a corresponding increase in request volume.

**Why this matters:**  
Token usage directly impacts inference cost and may signal inefficient prompts or routing regressions.

**Primary Signals:**  
- Token usage trends
- Request volume comparison

**Immediate Actions:**  
- Review recent prompt modifications  
- Validate routing logic and fallback behavior  
- Assess cost impact and rollback if necessary

