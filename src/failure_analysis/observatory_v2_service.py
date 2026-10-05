"""Experiment-aware Failure Observatory service."""

from __future__ import annotations

from dataclasses import dataclass

from src.failure_analysis.models import Failure
from src.failure_analysis.observatory_v2 import (
    FailureDimensionSummary,
    FailureRegression,
    ObservatoryAnalysis,
    analyze_experiment,
    compare_failure_rates,
    dimension_rates,
    dimension_summary,
)


@dataclass(frozen=True)
class FailureObservatoryV2:
    failures: tuple[Failure, ...]
    run_to_experiment: dict[str, str]
    question_metadata: dict[str, dict]

    def for_experiment(self, experiment_id: str) -> ObservatoryAnalysis:
        return analyze_experiment(
            self.failures,
            experiment_id=experiment_id,
            run_to_experiment=self.run_to_experiment,
            question_metadata=self.question_metadata,
        )

    def by_dimension(self, dimension: str, *, experiment_id: str | None = None) -> tuple[FailureDimensionSummary, ...]:
        failures = self.failures
        if experiment_id is not None:
            failures = tuple(
                failure for failure in failures
                if self.run_to_experiment.get(failure.run_id) == experiment_id
            )
        return dimension_summary(
            failures,
            dimension=dimension,
            question_metadata=self.question_metadata,
        )

    def rates(
        self,
        dimension: str,
        *,
        experiment_id: str,
        question_count: int,
    ):
        failures = tuple(
            failure for failure in self.failures
            if self.run_to_experiment.get(failure.run_id) == experiment_id
        )
        return dimension_rates(
            failures,
            dimension=dimension,
            question_count=question_count,
            question_metadata=self.question_metadata,
        )

    def regression(
        self,
        baseline_experiment_id: str,
        candidate_experiment_id: str,
        *,
        baseline_question_count: int,
        candidate_question_count: int,
        regression_threshold: float = 0.10,
    ) -> tuple[FailureRegression, ...]:
        baseline = tuple(
            failure for failure in self.failures
            if self.run_to_experiment.get(failure.run_id) == baseline_experiment_id
        )
        candidate = tuple(
            failure for failure in self.failures
            if self.run_to_experiment.get(failure.run_id) == candidate_experiment_id
        )
        return compare_failure_rates(
            baseline,
            candidate,
            baseline_question_count=baseline_question_count,
            candidate_question_count=candidate_question_count,
            regression_threshold=regression_threshold,
        )
