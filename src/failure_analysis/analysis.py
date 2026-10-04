"""Deterministic analysis operations over structured failures."""

from collections import Counter
from dataclasses import dataclass

from .models import Failure, FailureSeverity
from .store import FailureStore


@dataclass(frozen=True)
class FailureSummary:
    total: int
    by_category: dict[str, int]
    by_type: dict[str, int]
    by_severity: dict[str, int]

    def to_dict(self) -> dict:
        return {
            "total": self.total,
            "by_category": dict(self.by_category),
            "by_type": dict(self.by_type),
            "by_severity": dict(self.by_severity),
        }


def filter_failures(
    failures: list[Failure] | tuple[Failure, ...],
    *,
    category: str | None = None,
    failure_type: str | None = None,
    severity: FailureSeverity | str | None = None,
    run_id: str | None = None,
    question_id: str | None = None,
) -> list[Failure]:
    """Filter failures using exact, deterministic field matching."""
    if severity is not None:
        severity = FailureSeverity(severity)

    filters = {
        "category": category,
        "type": failure_type,
        "severity": severity,
        "run_id": run_id,
        "question_id": question_id,
    }

    for name, value in filters.items():
        if value is not None and (not isinstance(value, str) or not value.strip()) and name != "severity":
            raise ValueError(f"{name} filter must not be empty")

    return [
        failure
        for failure in sorted(failures, key=lambda item: item.failure_id)
        if (category is None or failure.category == category)
        and (failure_type is None or failure.type == failure_type)
        and (severity is None or failure.severity == severity)
        and (run_id is None or failure.run_id == run_id)
        and (question_id is None or failure.question_id == question_id)
    ]


def summarize_failures(failures: list[Failure] | tuple[Failure, ...]) -> FailureSummary:
    """Build deterministic counts by category, type, and severity."""
    ordered = sorted(failures, key=lambda item: item.failure_id)
    return FailureSummary(
        total=len(ordered),
        by_category=dict(sorted(Counter(f.category for f in ordered).items())),
        by_type=dict(sorted(Counter(f.type for f in ordered).items())),
        by_severity={
            severity.value: sum(f.severity == severity for f in ordered)
            for severity in FailureSeverity
            if any(f.severity == severity for f in ordered)
        },
    )


def analyze_store(
    store: FailureStore,
    *,
    category: str | None = None,
    failure_type: str | None = None,
    severity: FailureSeverity | str | None = None,
    run_id: str | None = None,
    question_id: str | None = None,
) -> FailureSummary:
    """Summarize persisted failures after applying exact filters."""
    failures = filter_failures(
        store.list(),
        category=category,
        failure_type=failure_type,
        severity=severity,
        run_id=run_id,
        question_id=question_id,
    )
    return summarize_failures(failures)
