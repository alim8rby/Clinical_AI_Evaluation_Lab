"""Benchmark-facing reliability evaluation."""
from dataclasses import dataclass

from src.evaluation.grounding_metrics import GroundingMetrics
from src.evaluation.reliability_metrics import ReliabilityMetrics, evaluate_reliability
from src.generation.models import Answer


@dataclass(frozen=True)
class ReliabilityEvaluation:
    answer_id: str
    metrics: ReliabilityMetrics
    evaluator_version: str = "reliability-v1"


def evaluate_answer_reliability(
    answer_id: str,
    answer: Answer,
    grounding: GroundingMetrics,
) -> ReliabilityEvaluation:
    return ReliabilityEvaluation(
        answer_id=answer_id,
        metrics=evaluate_reliability(answer, grounding),
    )
