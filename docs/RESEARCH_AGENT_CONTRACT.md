## Research Agents

Research Agents are responsible for **doing the actual research work** in the system.

Each Research Agent:
- Receives **one specific research task** from the planner  
- Collects **factual information only**
- Provides **evidence (sources)** for every claim
- Assigns a **confidence score** to its findings

Research Agents work **independently and in parallel**, meaning multiple tasks can be researched at the same time.

What Research Agents **do not** do:
- They do not make decisions
- They do not give recommendations
- They do not combine or summarize other agents’ work
- They do not think about the final answer

Their output is passed to the **Critic Agent** for validation and later combined by the **Synthesizer Agent** into a final, decision-ready report.

This design keeps research **modular, reliable, and scalable**, which is how real-world multi-agent AI systems are built.
