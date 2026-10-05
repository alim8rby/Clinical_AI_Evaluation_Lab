"""Batch experiment reporting."""

from __future__ import annotations

from dataclasses import dataclass

from src.evaluation.report import EvaluationReport, build_report
from src.experiments.engine import BatchRun, batch_configuration
from src.experiments.models import Experiment


@dataclass(frozen=True)
class BatchExperimentReport:
    evaluation: EvaluationReport
    batch: BatchRun
    configuration: dict


def build_batch_report(
    experiment: Experiment,
    batch: BatchRun,
    *,
    failures=None,
) -> BatchExperimentReport:
    report = build_report(
        experiment,
        list(batch.results),
        failures=failures,
    )
    return BatchExperimentReport(
        evaluation=report,
        batch=batch,
        configuration=batch_configuration(experiment),
    )


def render_batch_markdown(report: BatchExperimentReport) -> str:
    evaluation = report.evaluation
    lines = [
        f"# {evaluation.title}",
        "",
        f"- Experiment: {evaluation.experiment_id}",
        f"- Benchmark: {evaluation.benchmark_version}",
        f"- Requested questions: {report.batch.total_questions}",
        f"- Completed questions: {report.batch.completed_questions}",
        f"- Failed questions: {report.batch.failed_questions}",
        f"- Success rate: {report.batch.success_rate:.4f}",
        "",
        "## Configuration",
        "",
    ]
    for name, value in report.configuration.items():
        lines.append(f"- **{name}:** {value}")

    lines += ["", "## Aggregate Metrics", ""]
    if evaluation.metrics:
        lines += ["| Metric | Value |", "|---|---:|"]
        lines += [
            f"| {name} | {value:.4f} |"
            for name, value in evaluation.metrics.items()
        ]
    else:
        lines.append("No evaluation metrics recorded.")

    lines += ["", "## Recorded Failures", ""]
    lines += (
        [f"- {failure}" for failure in evaluation.failures]
        if evaluation.failures
        else ["No recorded failures."]
    )

    lines += ["", "## Batch Errors", ""]
    lines += (
        [f"- **{item['question_id']}**: {item['error_type']}: {item['error']}" for item in report.batch.errors]
        if report.batch.errors
        else ["No batch errors."]
    )
    return "\n".join(lines) + "\n"
