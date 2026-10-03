from typing import Protocol

from src.retrieval.search import EvidenceSet
from .models import Answer

class GenerationProvider(Protocol):
    def generate(self, question: str, evidence: EvidenceSet, *, prompt_version: str) -> Answer:
        ...

class MockGenerationProvider:
    """Deterministic provider used for local development and tests."""

    model = "mock-v1"

    def generate(self, question: str, evidence: EvidenceSet, *, prompt_version: str) -> Answer:
        if not question.strip():
            raise ValueError("question must not be empty")
        if not evidence.evidence:
            raise ValueError("evidence must not be empty")

        claims = [
            {
                "text": item.chunk.text,
                "citation_indices": [index],
            }
            for index, item in enumerate(evidence.evidence, start=1)
        ]
        from .models import Claim
        return Answer(
            answer_text="Based on the retrieved evidence: " + " ".join(c["text"] for c in claims),
            claims=[Claim(**claim) for claim in claims],
            uncertainty="Generated with the local deterministic development provider.",
            model=self.model,
            prompt_version=prompt_version,
        )
