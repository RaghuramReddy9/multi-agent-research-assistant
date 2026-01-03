from typing import List
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from src.state import GraphState


PLANNER_SYSTEM_PROMPT = """
You are a senior research planner.

Your job is to break a vague research question into
clear, independent, actionable research tasks.

Rules:
- Produce 3 to 6 tasks
- Each task must be researchable independently
- Tasks must be concise and concrete
- Do NOT include recommendations or conclusions
-  Output ONLY the task titles
- Do NOT include introductions, explanations, or commentary
- Each line must be a single research task
- No markdown, no bold text
"""


def planner_node(state: GraphState, llm) -> GraphState:
    """
    Planner node:
    - Reads user_query
    - Generates a structured research plan
    - Writes plan back into state
    """
    prompt = ChatPromptTemplate.from_messages(
        [
        ("system", PLANNER_SYSTEM_PROMPT),
        ("human", "{user_query}"),
        ]
    )

    chain = prompt | llm | StrOutputParser()

    raw_plan = chain.invoke({"user_query": state["user_query"]})

    plan = _parse_plan(raw_plan)

    state["plan"] = plan
    return state


def _parse_plan(text: str) -> List[str]:
    """
    Converts numbered or bullet text into a clean list of tasks.
    Filters out introductions and formatting noise.
    """
    tasks = []

    for line in text.split("\n"):
        line = line.strip()

        if not line:
            continue

        # Remove numbering
        line = line.lstrip("0123456789.- ").strip()

        # Filter out non-task lines
        if len(line.split()) < 3:
            continue

        if line.lower().startswith(("here are", "these are", "the following")):
            continue
        # Remove markdown emphasis
        line = line.replace("**", "")

        # Remove trailing colon
        if line.endswith(":"):
            line = line[:-1].strip()

        tasks.append(line)

    return tasks

