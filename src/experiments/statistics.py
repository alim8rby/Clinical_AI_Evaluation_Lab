"""Statistical comparison reports for experiment pairs."""

from __future__ import annotations

from dataclasses import dataclass

from src.evaluation.statistics import PairedStatistic, extract_metric_by_question, paired_compare


@dataclass(frozen=True)
class StatisticalComparison:
    baseline_experiment_id: str
    candidate_experiment_id: str
    benchmark_version: str
    comparisons: tuple[PairedStatistic, ...]


def compare_experiment_results(
    baseline_experiment_id: str,
    baseline_results: list[object],
    candidate_experiment_id: str,
    candidate_results: list[object],
    *,
    benchmark_version: str,
    metrics: list[tuple[str, str]],
    confidence_level: float = 0.95,
    bootstrap_iterations: int = 2000,
    seed: int = 2026,
) -> StatisticalComparison:
    if not baseline_experiment_id.strip() or not candidate_experiment_id.strip():
        raise ValueError("experiment IDs must not be empty")
    if not benchmark_version.strip():
        raise ValueError("benchmark_version must not be empty")
    if not metrics:
        raise ValueError("metrics must not be empty")

    comparisons = []
    for group, name in metrics:
        baseline = extract_metric_by_question(
            baseline_results, metric_group=group, metric_name=name
        )
        candidate = extract_metric_by_question(
            candidate_results, metric_group=group, metric_name=name
        )
        comparisons.append(
            paired_compare(
                f"{group}.{name}",
                baseline,
                candidate,
                confidence_level=confidence_level,
                bootstrap_iterations=bootstrap_iterations,
                seed=seed,
            )
        )

    return StatisticalComparison(
        baseline_experiment_id=baseline_experiment_id,
        candidate_experiment_id=candidate_experiment_id,
        benchmark_version=benchmark_version,
        comparisons=tuple(comparisons),
    )


def render_statistical_markdown(report: StatisticalComparison) -> str:
    lines = [
        "# Statistical Experiment Comparison",
        "",
        f"- Baseline: {report.baseline_experiment_id}",
        f"- Candidate: {report.candidate_experiment_id}",
        f"- Benchmark: {report.benchmark_version}",
        "",
        "## Paired Comparisons",
        "",
        "| Metric | N | Baseline mean | Candidate mean | Mean difference | CI low | CI high | Cohen dz |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for item in report.comparisons:
        lines.append(
            f"| {item.metric} | {item.n} | {item.baseline_mean:.4f} | "
            f"{item.candidate_mean:.4f} | {item.mean_difference:.4f} | "
            f"{item.ci_low:.4f} | {item.ci_high:.4f} | {item.effect_size_dz:.4f} |"
        )
    lines += [
        "",
        "CI = bootstrap confidence interval. Differences are candidate minus baseline.",
        "No composite score or statistical significance claim is produced by this report.",
    ]
    return "\n".join(lines) + "\n"
