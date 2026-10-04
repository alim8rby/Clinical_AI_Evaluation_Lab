"""Provider boundary for model-assisted semantic evaluation."""
from __future__ import annotations

from typing import Protocol


class SemanticEvaluationProvider(Protocol):
    evaluator_version: str

    def evaluate_answer(
        self,
        *,
        question: str,
        reference_answer: str,
        key_concepts: list[str],
        answer_text: str,
    ) -> dict[str, float]:
        """Return correctness, completeness, and relevance in [0, 1]."""

    def evaluate_grounding(
        self,
        *,
        question: str,
        answer_text: str,
        claims: list[dict],
        evidence: list[str],
    ) -> dict[str, float]:
        """Return faithfulness and unsupported_claim_rate in [0, 1]."""
