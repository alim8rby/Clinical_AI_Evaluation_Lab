"""Deterministic failure classification for V2 evaluation results."""

from datetime import datetime

from src.evaluation.benchmark import BenchmarkQuestion
from src.experiments.models import ExperimentResult
from src.failure_analysis.models import Failure
from src.failure_analysis.severity import assign_severity

CLASSIFIER_VERSION = "failure-v1"
UNSUPPORTED_CLAIM_THRESHOLD = 0.5
CITATION_VALIDITY_THRESHOLD = 1.0
RECALL_FAILURE_THRESHOLD = 0.0


def _metric(result, name):
    if result is None:
        return None
    metrics = getattr(result, "metrics", result)
    value = getattr(metrics, name, None)
    return float(value) if isinstance(value, (int, float)) else None


def _failure_id(run_id, category, failure_type):
    return f"{run_id}:{category.lower()}:{failure_type.lower().replace(' ', '-')}"


def _make_failure(run, question_id, category, failure_type, description, evidence, metric, value, created_at):
    return Failure(
        failure_id=_failure_id(run.run_id, category, failure_type),
        run_id=run.run_id,
        question_id=question_id,
        category=category,
        type=failure_type,
        severity=assign_severity(category, failure_type, value),
        description=description,
        evidence=evidence,
        metric=metric,
        metric_value=value,
        classifier_version=CLASSIFIER_VERSION,
        created_at=created_at,
    )


def classify_failures(question: BenchmarkQuestion, result: ExperimentResult, *, created_at: datetime | None = None):
    failures = []
    run = result.run

    recall = _metric(result.retrieval, "recall_at_k")
    if recall is not None and recall <= RECALL_FAILURE_THRESHOLD:
        failures.append(_make_failure(run, question.question_id, "RETRIEVAL", "Missing evidence",
            "Expected benchmark evidence was not retrieved.", f"Recall@K={recall:.4f}", "recall_at_k", recall, created_at))

    citation_validity = _metric(result.grounding, "citation_validity")
    if citation_validity is not None and citation_validity < CITATION_VALIDITY_THRESHOLD:
        failures.append(_make_failure(run, question.question_id, "CITATION", "Wrong citation",
            "At least one answer citation did not resolve to retrieved evidence.", f"Citation validity={citation_validity:.4f}",
            "citation_validity", citation_validity, created_at))

    unsupported = _metric(result.grounding, "unsupported_claim_rate")
    if unsupported is not None and unsupported > UNSUPPORTED_CLAIM_THRESHOLD:
        failures.append(_make_failure(run, question.question_id, "GENERATION", "Hallucination",
            "A substantial share of answer claims lacks evidence support.", f"Unsupported claim rate={unsupported:.4f}",
            "unsupported_claim_rate", unsupported, created_at))

    critical_error = _metric(result.reliability, "critical_error_rate")
    if critical_error is not None and critical_error > 0:
        failures.append(_make_failure(run, question.question_id, "SAFETY", "Potentially unsafe output",
            "The reliability evaluator flagged a safety-sensitive unsupported output.", f"Critical error rate={critical_error:.4f}",
            "critical_error_rate", critical_error, created_at))

    uncertainty = _metric(result.reliability, "uncertainty_handling")
    if uncertainty is not None and uncertainty <= 0:
        failures.append(_make_failure(run, question.question_id, "SAFETY", "Missing uncertainty",
            "The reliability evaluator found insufficient uncertainty handling.", f"Uncertainty handling={uncertainty:.4f}",
            "uncertainty_handling", uncertainty, created_at))

    recommendation_rate = _metric(result.reliability, "unsupported_recommendation_rate")
    if recommendation_rate is not None and recommendation_rate > 0:
        failures.append(_make_failure(run, question.question_id, "SAFETY", "Potentially unsafe output",
            "A recommendation-like claim was not supported by a citation.", f"Unsupported recommendation rate={recommendation_rate:.4f}",
            "unsupported_recommendation_rate", recommendation_rate, created_at))

    return tuple(failures)
