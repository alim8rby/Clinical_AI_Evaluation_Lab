"""Versioned ClinicalQA-v2 benchmark model and validation."""

from __future__ import annotations

from dataclasses import dataclass


ALLOWED_DIFFICULTIES = frozenset({"easy", "medium", "hard"})
ALLOWED_QUESTION_TYPES = frozenset({"fact", "comparison", "reasoning", "scenario", "safety"})
REQUIRED_FIELDS = frozenset({
    "question_id",
    "question",
    "domain",
    "difficulty",
    "question_type",
    "safety_relevance",
    "expected_evidence",
    "reference_answer",
    "key_concepts",
})


class BenchmarkV2ValidationError(ValueError):
    """Raised when a ClinicalQA-v2 question is invalid."""


@dataclass(frozen=True)
class BenchmarkV2Question:
    question_id: str
    question: str
    domain: str
    difficulty: str
    question_type: str
    safety_relevance: bool
    expected_evidence: tuple[str, ...]
    reference_answer: str
    key_concepts: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.question_id.strip():
            raise BenchmarkV2ValidationError("question_id must not be empty")
        if not self.question.strip():
            raise BenchmarkV2ValidationError("question must not be empty")
        if self.domain != "depression":
            raise BenchmarkV2ValidationError("ClinicalQA-v2 domain must be depression")
        if self.difficulty not in ALLOWED_DIFFICULTIES:
            raise BenchmarkV2ValidationError("invalid difficulty")
        if self.question_type not in ALLOWED_QUESTION_TYPES:
            raise BenchmarkV2ValidationError("invalid question_type")
        if not isinstance(self.safety_relevance, bool):
            raise BenchmarkV2ValidationError("safety_relevance must be boolean")
        if not self.expected_evidence:
            raise BenchmarkV2ValidationError("expected_evidence must not be empty")
        if not self.reference_answer.strip():
            raise BenchmarkV2ValidationError("reference_answer must not be empty")
        if not self.key_concepts:
            raise BenchmarkV2ValidationError("key_concepts must not be empty")
        if any(not item.strip() for item in self.expected_evidence):
            raise BenchmarkV2ValidationError("expected_evidence contains an empty item")
        if any(not item.strip() for item in self.key_concepts):
            raise BenchmarkV2ValidationError("key_concepts contains an empty item")


def validate_benchmark_v2_payload(payload: object) -> list[BenchmarkV2Question]:
    if not isinstance(payload, list):
        raise BenchmarkV2ValidationError("benchmark must be a list")

    questions: list[BenchmarkV2Question] = []
    ids: set[str] = set()
    for item in payload:
        if not isinstance(item, dict) or set(item) != REQUIRED_FIELDS:
            raise BenchmarkV2ValidationError("benchmark question has invalid fields")
        question = BenchmarkV2Question(
            question_id=item["question_id"],
            question=item["question"],
            domain=item["domain"],
            difficulty=item["difficulty"],
            question_type=item["question_type"],
            safety_relevance=item["safety_relevance"],
            expected_evidence=tuple(item["expected_evidence"]),
            reference_answer=item["reference_answer"],
            key_concepts=tuple(item["key_concepts"]),
        )
        if question.question_id in ids:
            raise BenchmarkV2ValidationError("duplicate question_id")
        ids.add(question.question_id)
        questions.append(question)

    if not questions:
        raise BenchmarkV2ValidationError("benchmark must not be empty")
    return questions


def unresolved_evidence(
    questions: list[BenchmarkV2Question],
    available_chunk_ids: set[str],
) -> dict[str, list[str]]:
    unresolved: dict[str, list[str]] = {}
    for question in questions:
        missing = [
            chunk_id for chunk_id in question.expected_evidence
            if chunk_id not in available_chunk_ids
        ]
        if missing:
            unresolved[question.question_id] = missing
    return unresolved


def assert_evidence_resolved(
    questions: list[BenchmarkV2Question],
    available_chunk_ids: set[str],
) -> None:
    unresolved = unresolved_evidence(questions, available_chunk_ids)
    if unresolved:
        raise BenchmarkV2ValidationError(
            f"unresolved expected evidence: {unresolved}"
        )
