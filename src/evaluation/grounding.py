"""Benchmark-facing grounding evaluation."""
from dataclasses import dataclass

from src.evaluation.grounding_metrics import GroundingMetrics, evaluate_grounding
from src.generation.citations import Citation
from src.generation.models import Answer
from src.retrieval.search import EvidenceSet
from src.evaluation.semantic import SemanticEvaluationProvider


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
    semantic_evaluator: SemanticEvaluationProvider | None = None,
) -> GroundingEvaluation:
    metrics = evaluate_grounding(answer, citations, evidence)
    if semantic_evaluator is not None:
        scores = semantic_evaluator.evaluate_grounding(
            question=evidence.query,
            answer_text=answer.answer_text,
            claims=[{"text": claim.text, "citation_indices": list(claim.citation_indices)} for claim in answer.claims],
            evidence=[item.chunk.text for item in evidence.evidence],
        )
        metrics = GroundingMetrics(
            citation_coverage=metrics.citation_coverage,
            citation_validity=metrics.citation_validity,
            faithfulness=metrics.faithfulness,
            unsupported_claim_rate=metrics.unsupported_claim_rate,
            semantic_faithfulness=scores["faithfulness"],
            semantic_unsupported_claim_rate=scores["unsupported_claim_rate"],
        )
    return GroundingEvaluation(
        answer_id=answer_id,
        metrics=metrics,
        evaluator_version=(
            f"{semantic_evaluator.evaluator_version}+grounding-v1" if semantic_evaluator else "grounding-v1"
        ),
    )
