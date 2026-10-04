"""Deterministic answer-quality metrics for ClinicalQA-v1."""
from dataclasses import dataclass
import re


@dataclass(frozen=True)
class AnswerMetrics:
    correctness: float
    completeness: float
    relevance: float


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def _validate(reference_answer: str, answer_text: str, key_concepts: list[str] | tuple[str, ...]) -> None:
    if not reference_answer.strip():
        raise ValueError("reference_answer must not be empty")
    if not answer_text.strip():
        raise ValueError("answer_text must not be empty")
    if not key_concepts:
        raise ValueError("key_concepts must not be empty")


def correctness_score(reference_answer: str, answer_text: str) -> float:
    reference = _tokens(reference_answer)
    answer = _tokens(answer_text)
    if not reference:
        return 0.0
    return len(reference & answer) / len(reference)


def completeness_score(answer_text: str, key_concepts: list[str] | tuple[str, ...]) -> float:
    answer = answer_text.lower()
    return sum(concept.lower() in answer for concept in key_concepts) / len(key_concepts)


def relevance_score(reference_answer: str, answer_text: str) -> float:
    reference = _tokens(reference_answer)
    answer = _tokens(answer_text)
    if not answer:
        return 0.0
    return len(reference & answer) / len(answer)


def evaluate_answer(
    reference_answer: str,
    answer_text: str,
    key_concepts: list[str] | tuple[str, ...],
) -> AnswerMetrics:
    _validate(reference_answer, answer_text, key_concepts)
    return AnswerMetrics(
        correctness=correctness_score(reference_answer, answer_text),
        completeness=completeness_score(answer_text, key_concepts),
        relevance=relevance_score(reference_answer, answer_text),
    )
