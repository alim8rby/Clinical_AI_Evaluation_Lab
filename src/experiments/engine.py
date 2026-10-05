"""Reproducible batch experiment orchestration."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable, Protocol

from src.experiments.models import Experiment, ExperimentResult


class QuestionRunner(Protocol):
    def __call__(self, experiment: Experiment, question: object) -> object:
        ...


@dataclass(frozen=True)
class BatchRun:
    experiment_id: str
    started_at: datetime
    finished_at: datetime
    total_questions: int
    completed_questions: int
    failed_questions: int
    results: tuple[ExperimentResult, ...]
    errors: tuple[dict, ...]

    @property
    def success_rate(self) -> float:
        if not self.total_questions:
            return 0.0
        return self.completed_questions / self.total_questions


def run_batch(
    experiment: Experiment,
    questions: list[object],
    runner: QuestionRunner,
    *,
    stop_on_error: bool = False,
) -> BatchRun:
    if not questions:
        raise ValueError("questions must not be empty")

    question_ids = [getattr(question, "question_id", None) for question in questions]
    if any(not question_id for question_id in question_ids):
        raise ValueError("every question must expose question_id")
    if len(question_ids) != len(set(question_ids)):
        raise ValueError("question IDs must be unique within a batch")

    started = datetime.now(timezone.utc).replace(tzinfo=None)
    results: list[ExperimentResult] = []
    errors: list[dict] = []

    for question in questions:
        question_id = question.question_id
        try:
            runtime_result = runner(experiment, question)
            result = getattr(runtime_result, "result", runtime_result)
            if not isinstance(result, ExperimentResult):
                raise TypeError("runner must return RuntimeResult or ExperimentResult")
            results.append(result)
        except Exception as exc:
            errors.append({
                "question_id": question_id,
                "error_type": type(exc).__name__,
                "error": str(exc),
            })
            if stop_on_error:
                break

    finished = datetime.now(timezone.utc).replace(tzinfo=None)
    return BatchRun(
        experiment_id=experiment.experiment_id,
        started_at=started,
        finished_at=finished,
        total_questions=len(questions),
        completed_questions=len(results),
        failed_questions=len(errors),
        results=tuple(results),
        errors=tuple(errors),
    )


def batch_configuration(experiment: Experiment) -> dict:
    """Return a stable, serializable experiment configuration snapshot."""
    return {
        "experiment_id": experiment.experiment_id,
        "name": experiment.name,
        "description": experiment.description,
        "model_config": experiment.config.model_config,
        "embedding_config": experiment.config.embedding_config,
        "retriever_config": experiment.config.retriever_config,
        "top_k": experiment.config.top_k,
        "prompt_version": experiment.config.prompt_version,
        "benchmark_version": experiment.config.benchmark_version,
        "created_at": experiment.created_at.isoformat(),
    }
