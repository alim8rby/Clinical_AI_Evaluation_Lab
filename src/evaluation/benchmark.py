"""Benchmark models and validation for ClinicalQA-v1."""
from dataclasses import dataclass

ALLOWED_DIFFICULTIES = frozenset({"easy", "medium", "hard"})
REQUIRED_FIELDS = frozenset({
    "question_id", "question", "domain", "difficulty",
    "expected_evidence", "reference_answer", "key_concepts",
})

class BenchmarkValidationError(ValueError):
    """Raised when a benchmark question is invalid."""

@dataclass(frozen=True)
class BenchmarkQuestion:
    question_id: str
    question: str
    domain: str
    difficulty: str
    expected_evidence: tuple[str, ...]
    reference_answer: str
    key_concepts: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.question_id.strip():
            raise BenchmarkValidationError("question_id must not be empty")
        if not self.question.strip():
            raise BenchmarkValidationError("question must not be empty")
        if self.domain != "depression":
            raise BenchmarkValidationError("ClinicalQA-v1 domain must be depression")
        if self.difficulty not in ALLOWED_DIFFICULTIES:
            raise BenchmarkValidationError("invalid difficulty")
        if not self.expected_evidence:
            raise BenchmarkValidationError("expected_evidence must not be empty")
        if not self.reference_answer.strip():
            raise BenchmarkValidationError("reference_answer must not be empty")
        if not self.key_concepts:
            raise BenchmarkValidationError("key_concepts must not be empty")
        if any(not item.strip() for item in self.expected_evidence):
            raise BenchmarkValidationError("expected_evidence contains an empty item")
        if any(not item.strip() for item in self.key_concepts):
            raise BenchmarkValidationError("key_concepts contains an empty item")

def validate_benchmark_payload(payload: object) -> list[BenchmarkQuestion]:
    if not isinstance(payload, list):
        raise BenchmarkValidationError("benchmark must be a list")
    questions = []
    ids = set()
    for item in payload:
        if not isinstance(item, dict) or set(item) != REQUIRED_FIELDS:
            raise BenchmarkValidationError("benchmark question has invalid fields")
        question = BenchmarkQuestion(
            question_id=item["question_id"],
            question=item["question"],
            domain=item["domain"],
            difficulty=item["difficulty"],
            expected_evidence=tuple(item["expected_evidence"]),
            reference_answer=item["reference_answer"],
            key_concepts=tuple(item["key_concepts"]),
        )
        if question.question_id in ids:
            raise BenchmarkValidationError("duplicate question_id")
        ids.add(question.question_id)
        questions.append(question)
    if not questions:
        raise BenchmarkValidationError("benchmark must not be empty")
    return questions
