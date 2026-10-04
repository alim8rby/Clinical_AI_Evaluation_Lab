"""Integrated V3 failure-analysis workflow.

This module connects classification, local persistence, and observatory reads
without introducing an HTTP or database dependency.
"""

from dataclasses import dataclass
from datetime import datetime

from src.evaluation.benchmark import BenchmarkQuestion
from src.experiments.models import ExperimentResult

from .classifier import classify_failures
from .models import Failure
from .observatory import FailureObservatory
from .store import FailureStore


@dataclass(frozen=True)
class FailureWorkflowResult:
    """Output of processing one evaluated experiment result."""

    failures: tuple[Failure, ...]
    result: ExperimentResult

    def __post_init__(self) -> None:
        if not all(isinstance(failure, Failure) for failure in self.failures):
            raise TypeError("failures must contain Failure records")


def process_result(
    question: BenchmarkQuestion,
    result: ExperimentResult,
    store: FailureStore,
    *,
    created_at: datetime | None = None,
) -> FailureWorkflowResult:
    """Classify an evaluation result, persist failures, and retain them on the run result."""
    failures = classify_failures(question, result, created_at=created_at)
    store.save_many(failures)
    updated_result = ExperimentResult(
        run=result.run,
        retrieval=result.retrieval,
        answer=result.answer,
        grounding=result.grounding,
        reliability=result.reliability,
        failures=tuple(failure.to_dict() for failure in failures),
    )
    return FailureWorkflowResult(failures=failures, result=updated_result)


def build_observatory(store: FailureStore) -> FailureObservatory:
    """Create the read boundary consumed by the Failure Observatory UI."""
    return FailureObservatory(store)
