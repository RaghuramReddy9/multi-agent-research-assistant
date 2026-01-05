from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from src.state import GraphState
from src.parsers import parse_research_output



RESEARCH_SYSTEM_PROMPT = """
You are a research assistant.

Your job is to research the given task and return factual findings only.

Rules:
- Focus ONLY on the given task
- Provide factual statements, not opinions
- Each finding must include supporting evidence
- Assign a confidence score between 0.0 and 1.0
- Do NOT provide recommendations or conclusions
- Do NOT reference other tasks

Output format:
Each finding must be written as:
- Summary: <factual statement>
- Evidence: <comma-separated sources>
- Confidence: <number>
"""


def research_node(state: GraphState, llm) -> GraphState:
    """
    Research node:
    - Executes one research task
    - Stores structured findings in shared state
    """
    task = state["current_task"].strip()
    if not task:
        return state

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", RESEARCH_SYSTEM_PROMPT),
            ("human", "{task}"),
        ]
    )

    chain = prompt | llm | StrOutputParser()

    raw_output = chain.invoke({"task": task})

    findings = parse_research_output(raw_output)

    if not findings:
        state["research_results"][task] = []
        state["quality_flags"][task] = "no_valid_findings"
        return state

    state["research_results"][task] = findings
    return state

