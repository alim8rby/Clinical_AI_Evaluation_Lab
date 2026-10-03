PROMPT_VERSION = "v1"

SYSTEM_PROMPT = """You are a clinical question-answering system.
Answer only from the supplied evidence.
Do not invent facts or citations.
Clearly state uncertainty when the evidence is insufficient.
Every substantive claim must reference one or more supplied evidence items.
This output supports evaluation and is not an autonomous clinical decision.
"""

def build_prompt(question: str, evidence_text: str) -> str:
    if not question.strip():
        raise ValueError("question must not be empty")
    if not evidence_text.strip():
        raise ValueError("evidence_text must not be empty")
    return f"{SYSTEM_PROMPT}\n\nQuestion:\n{question.strip()}\n\nEvidence:\n{evidence_text.strip()}"
