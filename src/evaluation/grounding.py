"""Benchmark-facing grounding evaluation."""
from dataclasses import dataclass

from src.evaluation.grounding_metrics import GroundingMetrics, evaluate_grounding
from src.generation.citations import Citation
from src.generation.models import Answer
from src.retrieval.search import EvidenceSet


@dataclass(frozen=True)
class GroundingEvaluation:
    answer_id: str
    metrics: GroundingMetrics
    evaluator_version: str = "grounding-v1"


def evaluate_answer_grounding(
    answer_id: str,
    answer: Answer,
    citations: list[Citation],
    evidence: EvidenceSet,
) -> GroundingEvaluation:
    return GroundingEvaluation(
        answer_id=answer_id,
        metrics=evaluate_grounding(answer, citations, evidence),
    )
