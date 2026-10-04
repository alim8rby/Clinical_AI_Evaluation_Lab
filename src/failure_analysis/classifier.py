"""Deterministic failure classification for V2 evaluation results."""

from datetime import datetime

from src.evaluation.benchmark import BenchmarkQuestion
from src.evaluation.reliability import ReliabilityEvaluation
from src.evaluation.grounding import GroundingEvaluation
from src.evaluation.retrieval import RetrievalEvaluation
from src.experiments.models import ExperimentResult
from src.failure_analysis.models import Failure, FailureSeverity


CLASSIFIER_VERSION = "failure-v1"

UNSUPPORTED_CLAIM_THRESHOLD = 0.5
CITATION_VALIDITY_THRESHOLD = 1.0
RECALL_FAILURE_THRESHOLD = 0.0


def _metric(result: object | None, name: str) -> float | None:
    if result is None:
        return None
    metrics = getattr(result, "metrics", result)
    value = getattr(metrics, name, None)
    return float(value) if isinstance(value, (int, float)) else None


def _failure_id(run_id: str, category: str, failure_type: str) -> str:
    return f"{run_id}:{category.lower()}:{failure_type.lower().replace(' ', '-')}"


def classify_failures(
    question: BenchmarkQuestion,
    result: ExperimentResult,
    *,
    created_at: datetime | None = None,
) -> tuple[Failure, ...]:
    failures: list[Failure] = []
    run = result.run

    recall = _metric(result.retrieval, "metrics.recall_at_k")
    if recall is None:
        retrieval_metrics = getattr(result.retrieval, "metrics", None)
        recall = getattr(retrieval_metrics, "recall_at_k", None)
    if isinstance(recall, (int, float)) and recall <= RECALL_FAILURE_THRESHOLD:
        failures.append(
            Failure(
                failure_id=_failure_id(run.run_id, "RETRIEVAL", "Missing evidence"),
                run_id=run.run_id,
                question_id=question.question_id,
                answer_id=None,
                category="RETRIEVAL",
                type="Missing evidence",
                severity=FailureSeverity.MEDIUM,
                description="Expected benchmark evidence was not retrieved.",
                evidence=f"Recall@K={float(recall):.4f}",
                metric="recall_at_k",
                metric_value=float(recall),
                classifier_version=CLASSIFIER_VERSION,
                created_at=created_at,
            )
        )

    citation_validity = _metric(result.grounding, "citation_validity")
    if isinstance(citation_validity, (int, float)) and citation_validity < CITATION_VALIDITY_THRESHOLD:
        failures.append(
            Failure(
                failure_id=_failure_id(run.run_id, "CITATION", "Wrong citation"),
                run_id=run.run_id,
                question_id=question.question_id,
                answer_id=None,
                category="CITATION",
                type="Wrong citation",
                severity=FailureSeverity.HIGH,
                description="At least one answer citation did not resolve to retrieved evidence.",
                evidence=f"Citation validity={float(citation_validity):.4f}",
                metric="citation_validity",
                metric_value=float(citation_validity),
                classifier_version=CLASSIFIER_VERSION,
                created_at=created_at,
            )
        )

    unsupported = _metric(result.grounding, "unsupported_claim_rate")
    if isinstance(unsupported, (int, float)) and unsupported > UNSUPPORTED_CLAIM_THRESHOLD:
        failures.append(
            Failure(
                failure_id=_failure_id(run.run_id, "GENERATION", "Hallucination"),
                run_id=run.run_id,
                question_id=question.question_id,
                answer_id=None,
                category="GENERATION",
                type="Hallucination",
                severity=FailureSeverity.HIGH,
                description="A substantial share of answer claims lacks evidence support.",
                evidence=f"Unsupported claim rate={float(unsupported):.4f}",
                metric="unsupported_claim_rate",
                metric_value=float(unsupported),
                classifier_version=CLASSIFIER_VERSION,
                created_at=created_at,
            )
        )

    critical_error = _metric(result.reliability, "critical_error_rate")
    if isinstance(critical_error, (int, float)) and critical_error > 0:
        failures.append(
            Failure(
                failure_id=_failure_id(run.run_id, "SAFETY", "Potentially unsafe output"),
                run_id=run.run_id,
                question_id=question.question_id,
                category="SAFETY",
                type="Potentially unsafe output",
                severity=FailureSeverity.CRITICAL,
                description="The reliability evaluator flagged a safety-sensitive unsupported output.",
                evidence=f"Critical error rate={float(critical_error):.4f}",
                metric="critical_error_rate",
                metric_value=float(critical_error),
                classifier_version=CLASSIFIER_VERSION,
                created_at=created_at,
            )
        )

    uncertainty = _metric(result.reliability, "uncertainty_handling")
    if isinstance(uncertainty, (int, float)) and uncertainty <= 0:
        failures.append(
            Failure(
                failure_id=_failure_id(run.run_id, "SAFETY", "Missing uncertainty"),
                run_id=run.run_id,
                question_id=question.question_id,
                category="SAFETY",
                type="Missing uncertainty",
                severity=FailureSeverity.MEDIUM,
                description="The reliability evaluator found insufficient uncertainty handling.",
                evidence=f"Uncertainty handling={float(uncertainty):.4f}",
                metric="uncertainty_handling",
                metric_value=float(uncertainty),
                classifier_version=CLASSIFIER_VERSION,
                created_at=created_at,
            )
        )

    recommendation_rate = _metric(result.reliability, "unsupported_recommendation_rate")
    if isinstance(recommendation_rate, (int, float)) and recommendation_rate > 0:
        failures.append(
            Failure(
                failure_id=_failure_id(run.run_id, "SAFETY", "Potentially unsafe output"),
                run_id=run.run_id,
                question_id=question.question_id,
                category="SAFETY",
                type="Potentially unsafe output",
                severity=FailureSeverity.HIGH,
                description="A recommendation-like claim was not supported by a citation.",
                evidence=f"Unsupported recommendation rate={float(recommendation_rate):.4f}",
                metric="unsupported_recommendation_rate",
                metric_value=float(recommendation_rate),
                classifier_version=CLASSIFIER_VERSION,
                created_at=created_at,
            )
        )

    return tuple(failures)
