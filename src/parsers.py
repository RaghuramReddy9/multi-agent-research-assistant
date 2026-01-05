import re
from typing import List
from src.state import ResearchItem


def parse_research_output(text: str) -> List[ResearchItem]:
    """
    Robust parser that tolerates markdown and formatting variations.
    """

    findings: List[ResearchItem] = []

    # Split on blank lines (research items)
    blocks = re.split(r"\n\s*\n", text.strip())

    for block in blocks:
        summary = None
        evidence = []
        confidence = None

        # Summary: tolerate *, **, -, or plain text
        summary_match = re.search(
            r"(?:Summary:|\*\*Summary:\*\*|- Summary:)\s*(.+)",
            block,
            re.IGNORECASE,
        )

        evidence_match = re.search(
            r"(?:Evidence:|\*\*Evidence:\*\*|- Evidence:)\s*(.+)",
            block,
            re.IGNORECASE,
        )

        confidence_match = re.search(
            r"(?:Confidence:|\*\*Confidence:\*\*|- Confidence:)\s*([0-9.]+)",
            block,
            re.IGNORECASE,
        )

        if summary_match:
            summary = summary_match.group(1).strip()

        if evidence_match:
            evidence_text = evidence_match.group(1).strip()
            evidence = [e.strip() for e in re.split(r",|;", evidence_text) if e.strip()]

        if confidence_match:
            confidence = float(confidence_match.group(1))

        if summary and evidence and confidence is not None:
            findings.append(
                ResearchItem(
                    summary=summary,
                    evidence=evidence,
                    confidence=confidence,
                )
            )

    return findings
