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
class FailureRegression:
    category: str
    failure_type: str
    baseline_rate: float
    candidate_rate: float
    rate_difference: float
    baseline_questions: int
    candidate_questions: int
    regression: bool


@dataclass(frozen=True)
class ObservatoryAnalysis:
    experiment_id: str | None
    total_failures: int
    unique_questions: int
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


def analyze_experiment(
    failures: list[Failure] | tuple[Failure, ...],
    *,
    experiment_id: str,
    run_to_experiment: dict[str, str],
    question_metadata: dict[str, dict],
) -> ObservatoryAnalysis:
    if not experiment_id.strip():
        raise ValueError("experiment_id must not be empty")

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
    keys = sorted(set(baseline) | set(candidate))

    return tuple(
        FailureRegression(
            category=category,
            failure_type=failure_type,
            baseline_rate=baseline[(category, failure_type)] / baseline_question_count,
            candidate_rate=candidate[(category, failure_type)] / candidate_question_count,
            rate_difference=(
                candidate[(category, failure_type)] / candidate_question_count
                - baseline[(category, failure_type)] / baseline_question_count
            ),
            baseline_questions=baseline_question_count,
            candidate_questions=candidate_question_count,
            regression=(
                candidate[(category, failure_type)] / candidate_question_count
                - baseline[(category, failure_type)] / baseline_question_count
            ) >= regression_threshold,
        )
        for category, failure_type in keys
    )
