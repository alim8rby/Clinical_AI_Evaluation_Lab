"""Paired statistical analysis for controlled experiment comparisons."""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
import random
from statistics import mean


@dataclass(frozen=True)
class PairedStatistic:
    metric: str
    n: int
    baseline_mean: float
    candidate_mean: float
    mean_difference: float
    ci_low: float
    ci_high: float
    effect_size_dz: float
    bootstrap_iterations: int
    confidence_level: float


def _validate_pairs(
    baseline: dict[str, float],
    candidate: dict[str, float],
) -> list[tuple[str, float, float]]:
    if not baseline or not candidate:
        raise ValueError("baseline and candidate must not be empty")
    if set(baseline) != set(candidate):
        raise ValueError("baseline and candidate must contain the same question IDs")
    pairs = []
    for question_id in sorted(baseline):
        left = float(baseline[question_id])
        right = float(candidate[question_id])
        if not all(value == value for value in (left, right)):
            raise ValueError("paired values must not be NaN")
        pairs.append((question_id, left, right))
    return pairs


def _bootstrap_ci(
    differences: list[float],
    *,
    confidence_level: float,
    iterations: int,
    seed: int,
) -> tuple[float, float]:
    if iterations <= 0:
        raise ValueError("iterations must be greater than zero")
    if not 0.0 < confidence_level < 1.0:
        raise ValueError("confidence_level must be between 0 and 1")

    rng = random.Random(seed)
    samples = []
    for _ in range(iterations):
        resample = [differences[rng.randrange(len(differences))] for _ in differences]
        samples.append(mean(resample))
    samples.sort()

    alpha = 1.0 - confidence_level
    low_index = max(0, min(len(samples) - 1, int((alpha / 2) * len(samples))))
    high_index = max(
        0,
        min(len(samples) - 1, int((1 - alpha / 2) * len(samples)) - 1),
    )
    return samples[low_index], samples[high_index]


def paired_compare(
    metric: str,
    baseline: dict[str, float],
    candidate: dict[str, float],
    *,
    confidence_level: float = 0.95,
    bootstrap_iterations: int = 2000,
    seed: int = 2026,
) -> PairedStatistic:
    if not metric.strip():
        raise ValueError("metric must not be empty")
    pairs = _validate_pairs(baseline, candidate)
    differences = [candidate_value - baseline_value for _, baseline_value, candidate_value in pairs]
    n = len(differences)
    difference_mean = mean(differences)

    variance = (
        sum((difference - difference_mean) ** 2 for difference in differences) / (n - 1)
        if n > 1
        else 0.0
    )
    standard_deviation = sqrt(variance)
    effect_size = difference_mean / standard_deviation if standard_deviation else 0.0

    ci_low, ci_high = _bootstrap_ci(
        differences,
        confidence_level=confidence_level,
        iterations=bootstrap_iterations,
        seed=seed,
    )

    return PairedStatistic(
        metric=metric,
        n=n,
        baseline_mean=mean(baseline.values()),
        candidate_mean=mean(candidate.values()),
        mean_difference=difference_mean,
        ci_low=ci_low,
        ci_high=ci_high,
        effect_size_dz=effect_size,
        bootstrap_iterations=bootstrap_iterations,
        confidence_level=confidence_level,
    )


def extract_metric_by_question(
    results: list[object],
    *,
    metric_group: str,
    metric_name: str,
) -> dict[str, float]:
    if not results:
        raise ValueError("results must not be empty")
    values = {}
    for result in results:
        question_id = getattr(result.run, "question_id", None)
        if not question_id:
            raise ValueError("result run must expose question_id")
        group = getattr(result, metric_group, None)
        if group is None:
            raise ValueError(f"result has no metric group: {metric_group}")
        metrics = getattr(group, "metrics", group)
        value = getattr(metrics, metric_name, None)
        if not isinstance(value, (int, float)):
            raise ValueError(f"metric is not numeric: {metric_group}.{metric_name}")
        values[question_id] = float(value)
    if len(values) != len(results):
        raise ValueError("question IDs must be unique")
    return values
