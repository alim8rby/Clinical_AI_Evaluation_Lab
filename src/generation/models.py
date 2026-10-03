from dataclasses import dataclass

@dataclass(frozen=True)
class Claim:
    text: str
    citation_indices: list[int]

@dataclass(frozen=True)
class Answer:
    answer_text: str
    claims: list[Claim]
    uncertainty: str | None
    model: str
    prompt_version: str
