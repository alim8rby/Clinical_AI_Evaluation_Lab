"""Benchmark-facing answer evaluation."""
from dataclasses import dataclass

from src.evaluation.answer_metrics import AnswerMetrics, evaluate_answer
from src.evaluation.benchmark import BenchmarkQuestion
from src.generation.models import Answer


@dataclass(frozen=True)
class AnswerEvaluation:
    question_id: str
    metrics: AnswerMetrics
    evaluator_version: str = "answer-v1"


def evaluate_question_answer(
    question: BenchmarkQuestion,
    answer: Answer,
) -> AnswerEvaluation:
    metrics = evaluate_answer(
        question.reference_answer,
        answer.answer_text,
        question.key_concepts,
    )
    return AnswerEvaluation(
        question_id=question.question_id,
        metrics=metrics,
    )
