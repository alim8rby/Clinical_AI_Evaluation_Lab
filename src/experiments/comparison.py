"""Transparent experiment comparison."""
from dataclasses import dataclass

from src.experiments.models import Experiment, ExperimentResult


@dataclass(frozen=True)
class MetricDelta:
    metric: str
    baseline: float
    candidate: float
    delta: float


@dataclass(frozen=True)
class ExperimentComparison:
    baseline_experiment_id: str
    candidate_experiment_id: str
    benchmark_version: str
    metric_deltas: tuple[MetricDelta, ...]
    baseline_samples: int
    candidate_samples: int


def _metric_values(results: list[ExperimentResult]) -> dict[str, float]:
    values: dict[str, list[float]] = {}
    for result in results:
        for group_name in ("retrieval", "answer", "grounding", "reliability"):
            group = getattr(result, group_name)
            if group is None:
                continue
            metrics = getattr(group, "metrics", group)
            for name, value in vars(metrics).items():
                if isinstance(value, (int, float)):
                    values.setdefault(f"{group_name}.{name}", []).append(float(value))
    return {name: sum(items) / len(items) for name, items in values.items()}


def compare_experiments(
    baseline: Experiment,
    candidate: Experiment,
    baseline_results: list[ExperimentResult],
    candidate_results: list[ExperimentResult],
) -> ExperimentComparison:
    if baseline.config.benchmark_version != candidate.config.benchmark_version:
        raise ValueError("experiments must use the same benchmark version")
    if baseline.experiment_id == candidate.experiment_id:
        raise ValueError("baseline and candidate must be different experiments")

    baseline_values = _metric_values(baseline_results)
    candidate_values = _metric_values(candidate_results)
    shared_metrics = sorted(set(baseline_values) & set(candidate_values))
    deltas = tuple(
        MetricDelta(
            metric=name,
            baseline=baseline_values[name],
            candidate=candidate_values[name],
            delta=candidate_values[name] - baseline_values[name],
        )
        for name in shared_metrics
    )
    return ExperimentComparison(
        baseline_experiment_id=baseline.experiment_id,
        candidate_experiment_id=candidate.experiment_id,
        benchmark_version=baseline.config.benchmark_version,
        metric_deltas=deltas,
        baseline_samples=len(baseline_results),
        candidate_samples=len(candidate_results),
    )
