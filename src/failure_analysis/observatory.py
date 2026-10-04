"""UI-independent query service for the Failure Observatory."""

from dataclasses import dataclass

from .analysis import FailureSummary, filter_failures, summarize_failures
from .models import Failure, FailureSeverity
from .store import FailureStore


class FailureNotFoundError(LookupError):
    """Raised when an observatory lookup targets a missing failure."""


@dataclass(frozen=True)
class FailureQuery:
    category: str | None = None
    failure_type: str | None = None
    severity: FailureSeverity | str | None = None
    run_id: str | None = None
    question_id: str | None = None
    limit: int | None = None

    def __post_init__(self) -> None:
        if self.severity is not None:
            object.__setattr__(self, "severity", FailureSeverity(self.severity))
        if self.limit is not None and self.limit <= 0:
            raise ValueError("limit must be greater than zero")


@dataclass(frozen=True)
class FailureObservatorySnapshot:
    failures: tuple[Failure, ...]
    summary: FailureSummary

    def to_dict(self) -> dict:
        return {
            "failures": [failure.to_dict() for failure in self.failures],
            "summary": self.summary.to_dict(),
        }


class FailureObservatory:
    """Read-oriented service for Failure Observatory consumers."""

    def __init__(self, store: FailureStore) -> None:
        self.store = store

    def get_failure(self, failure_id: str) -> Failure:
        failure = self.store.get(failure_id)
        if failure is None:
            raise FailureNotFoundError(f"failure not found: {failure_id}")
        return failure

    def list_failures(self, query: FailureQuery | None = None) -> tuple[Failure, ...]:
        query = query or FailureQuery()
        failures = filter_failures(
            self.store.list(),
            category=query.category,
            failure_type=query.failure_type,
            severity=query.severity,
            run_id=query.run_id,
            question_id=query.question_id,
        )
        if query.limit is not None:
            failures = failures[:query.limit]
        return tuple(failures)

    def summary(self, query: FailureQuery | None = None) -> FailureSummary:
        return summarize_failures(self.list_failures(query))

    def snapshot(self, query: FailureQuery | None = None) -> FailureObservatorySnapshot:
        failures = self.list_failures(query)
        return FailureObservatorySnapshot(
            failures=failures,
            summary=summarize_failures(failures),
        )
