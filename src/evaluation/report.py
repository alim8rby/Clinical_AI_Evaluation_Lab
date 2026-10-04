"""Reproducible evaluation report generation."""
from dataclasses import dataclass

from src.experiments.models import ExperimentResult


@dataclass(frozen=True)
class EvaluationReport:
    title: str
    experiment_id: str
    benchmark_version: str
    configuration: dict
    sample_count: int
    metrics: dict[str, float]
    failures: tuple[dict, ...]


def _collect_metrics(results: list[ExperimentResult]) -> dict[str, float]:
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
    return {name: sum(items) / len(items) for name, items in sorted(values.items())}


def build_report(experiment, results, *, failures=None):
    return EvaluationReport(
        title=f"Evaluation Report - {experiment.name}",
        experiment_id=experiment.experiment_id,
        benchmark_version=experiment.config.benchmark_version,
        configuration={
            "model_config": experiment.config.model_config,
            "embedding_config": experiment.config.embedding_config,
            "retriever_config": experiment.config.retriever_config,
            "top_k": experiment.config.top_k,
            "prompt_version": experiment.config.prompt_version,
        },
        sample_count=len(results),
        metrics=_collect_metrics(results),
        failures=tuple(failures or []),
    )


def render_markdown(report):
    lines = [
        f"# {report.title}", "",
        f"- Experiment: {report.experiment_id}",
        f"- Benchmark: {report.benchmark_version}",
        f"- Samples: {report.sample_count}", "",
        "## Configuration", "",
    ]
    for name, value in report.configuration.items():
        lines.append(f"- **{name}:** {value}")
    lines.extend(["", "## Metrics", ""])
    if report.metrics:
        lines += ["| Metric | Value |", "|---|---:|"]
        for name, value in report.metrics.items():
            lines.append(f"| {name} | {value:.4f} |")
    else:
        lines.append("No evaluation metrics recorded.")
    lines.extend(["", "## Failures", ""])
    if report.failures:
        lines.extend(f"- {failure}" for failure in report.failures)
    else:
        lines.append("No failures recorded.")
    return "\n".join(lines) + "\n"
