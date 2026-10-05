"""Experiment-aware Failure Observatory 2.0 analysis."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from src.failure_analysis.models import Failure


@dataclass(frozen=True)
class FailureDimensionSummary:
    dimension: str
    value: str
    failure_count: int
    unique_questions: int


@dataclass(frozen=True)
class FailureDimensionRate:
    dimension: str
    value: str
    failure_count: int
    unique_questions: int
    question_count: int
    failure_rate: float


@dataclass(frozen=True)
class FailureRegression:
    category: str
    failure_type: str
    baseline_rate: float
    candidate_rate: float
    rate_difference: float
    baseline_questions: int
    candidate_questions: int
    regression: bool
    baseline_affected_questions: int = 0
    candidate_affected_questions: int = 0
    question_level_regression: bool = False


@dataclass(frozen=True)
class ObservatoryAnalysis:
    experiment_id: str | None
    total_failures: int
    unique_questions: int
    completed_questions: int | None
    by_category: dict[str, int]
    by_type: dict[str, int]
    by_severity: dict[str, int]
    by_difficulty: dict[str, int]
    by_question_type: dict[str, int]


def _count(
    failures: list[Failure],
    key,
) -> dict[str, int]:
    return dict(sorted(Counter(key(failure) for failure in failures).items()))


def _validate_question_count(question_count: int | None) -> None:
    if question_count is not None and question_count <= 0:
        raise ValueError("question count must be greater than zero")


def analyze_experiment(
    failures: list[Failure] | tuple[Failure, ...],
    *,
    experiment_id: str,
    run_to_experiment: dict[str, str],
    question_metadata: dict[str, dict],
    completed_question_count: int | None = None,
) -> ObservatoryAnalysis:
    if not experiment_id.strip():
        raise ValueError("experiment_id must not be empty")
    _validate_question_count(completed_question_count)

    selected = [
        failure
        for failure in failures
        if run_to_experiment.get(failure.run_id) == experiment_id
    ]
    unique_questions = {failure.question_id for failure in selected}

    return ObservatoryAnalysis(
        experiment_id=experiment_id,
        total_failures=len(selected),
        unique_questions=len(unique_questions),
        completed_questions=completed_question_count,
        by_category=_count(selected, lambda item: item.category),
        by_type=_count(selected, lambda item: item.type),
        by_severity=_count(selected, lambda item: item.severity.value),
        by_difficulty=_count(
            selected,
            lambda item: str(question_metadata.get(item.question_id, {}).get("difficulty", "unknown")),
        ),
        by_question_type=_count(
            selected,
            lambda item: str(question_metadata.get(item.question_id, {}).get("question_type", "unknown")),
        ),
    )


def dimension_summary(
    failures: list[Failure] | tuple[Failure, ...],
    *,
    dimension: str,
    question_metadata: dict[str, dict] | None = None,
) -> tuple[FailureDimensionSummary, ...]:
    if dimension not in {"category", "type", "severity", "difficulty", "question_type"}:
        raise ValueError("unsupported failure dimension")

    metadata = question_metadata or {}

    def value_for(failure: Failure) -> str:
        if dimension == "category":
            return failure.category
        if dimension == "type":
            return failure.type
        if dimension == "severity":
            return failure.severity.value
        return str(metadata.get(failure.question_id, {}).get(dimension, "unknown"))

    groups: dict[str, set[str]] = {}
    counts: Counter[str] = Counter()
    for failure in failures:
        value = value_for(failure)
        counts[value] += 1
        groups.setdefault(value, set()).add(failure.question_id)

    return tuple(
        FailureDimensionSummary(
            dimension=dimension,
            value=value,
            failure_count=counts[value],
            unique_questions=len(groups[value]),
        )
        for value in sorted(counts)
    )


def dimension_rates(
    failures: list[Failure] | tuple[Failure, ...],
    *,
    dimension: str,
    question_count: int,
    question_metadata: dict[str, dict] | None = None,
) -> tuple[FailureDimensionRate, ...]:
    if question_count <= 0:
        raise ValueError("question count must be greater than zero")

    return tuple(
        FailureDimensionRate(
            dimension=item.dimension,
            value=item.value,
            failure_count=item.failure_count,
            unique_questions=item.unique_questions,
            question_count=question_count,
            failure_rate=item.failure_count / question_count,
        )
        for item in dimension_summary(
            failures,
            dimension=dimension,
            question_metadata=question_metadata,
        )
    )


def compare_failure_rates(
    baseline_failures: list[Failure] | tuple[Failure, ...],
    candidate_failures: list[Failure] | tuple[Failure, ...],
    *,
    baseline_question_count: int,
    candidate_question_count: int,
    regression_threshold: float = 0.10,
) -> tuple[FailureRegression, ...]:
    if baseline_question_count <= 0 or candidate_question_count <= 0:
        raise ValueError("question counts must be greater than zero")
    if regression_threshold < 0:
        raise ValueError("regression_threshold must not be negative")

    baseline = Counter((failure.category, failure.type) for failure in baseline_failures)
    candidate = Counter((failure.category, failure.type) for failure in candidate_failures)
    baseline_questions = {
        key: {failure.question_id for failure in baseline_failures if (failure.category, failure.type) == key}
        for key in set(baseline)
    }
    candidate_questions = {
        key: {failure.question_id for failure in candidate_failures if (failure.category, failure.type) == key}
        for key in set(candidate)
    }
    keys = sorted(set(baseline) | set(candidate))

    return tuple(
        _build_regression(
            category,
            failure_type,
            baseline,
            candidate,
            baseline_questions,
            candidate_questions,
            baseline_question_count,
            candidate_question_count,
            regression_threshold,
        )
        for category, failure_type in keys
    )


def _build_regression(
    category: str,
    failure_type: str,
    baseline: Counter,
    candidate: Counter,
    baseline_questions: dict[tuple[str, str], set[str]],
    candidate_questions: dict[tuple[str, str], set[str]],
    baseline_question_count: int,
    candidate_question_count: int,
    regression_threshold: float,
) -> FailureRegression:
    key = (category, failure_type)
    baseline_rate = baseline[key] / baseline_question_count
    candidate_rate = candidate[key] / candidate_question_count
    baseline_affected = len(baseline_questions.get(key, set()))
    candidate_affected = len(candidate_questions.get(key, set()))
    question_regression = bool(
        candidate_questions.get(key, set()) - baseline_questions.get(key, set())
    )
    return FailureRegression(
        category=category,
        failure_type=failure_type,
        baseline_rate=baseline_rate,
        candidate_rate=candidate_rate,
        rate_difference=candidate_rate - baseline_rate,
        baseline_questions=baseline_question_count,
        candidate_questions=candidate_question_count,
        regression=(candidate_rate - baseline_rate) >= regression_threshold,
        baseline_affected_questions=baseline_affected,
        candidate_affected_questions=candidate_affected,
        question_level_regression=question_regression,
    )
