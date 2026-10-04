"""Benchmark-facing answer evaluation."""
from dataclasses import dataclass

from src.evaluation.answer_metrics import AnswerMetrics, evaluate_answer
from src.evaluation.benchmark import BenchmarkQuestion
from src.generation.models import Answer
from src.evaluation.semantic import SemanticEvaluationProvider


@dataclass(frozen=True)
class AnswerEvaluation:
    question_id: str
    metrics: AnswerMetrics
    evaluator_version: str = "answer-v1"


def evaluate_question_answer(
    question: BenchmarkQuestion,
    answer: Answer,
    semantic_evaluator: SemanticEvaluationProvider | None = None,
) -> AnswerEvaluation:
    metrics = evaluate_answer(
        question.reference_answer,
        answer.answer_text,
        question.key_concepts,
    )
    if semantic_evaluator is not None:
        scores = semantic_evaluator.evaluate_answer(
            question=question.question,
            reference_answer=question.reference_answer,
            key_concepts=list(question.key_concepts),
            answer_text=answer.answer_text,
        )
        metrics = AnswerMetrics(
            correctness=metrics.correctness,
            completeness=metrics.completeness,
            relevance=metrics.relevance,
            semantic_correctness=scores["correctness"],
            semantic_completeness=scores["completeness"],
            semantic_relevance=scores["relevance"],
        )
    return AnswerEvaluation(question_id=question.question_id, metrics=metrics, evaluator_version=(
        f"{semantic_evaluator.evaluator_version}+answer-v1" if semantic_evaluator else "answer-v1"
    ))
