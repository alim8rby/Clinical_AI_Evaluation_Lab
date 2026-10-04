"""Validation for the V4.14 retrieval challenge set."""
from __future__ import annotations

from dataclasses import dataclass


REQUIRED_FIELDS = frozenset({
    "case_id", "question", "challenge_type",
    "expected_evidence", "distractor_evidence", "difficulty",
})
ALLOWED_TYPES = frozenset({"lexical_mismatch", "multi_evidence", "ranking"})
ALLOWED_DIFFICULTIES = frozenset({"easy", "medium", "hard"})


class RetrievalChallengeValidationError(ValueError):
    pass


@dataclass(frozen=True)
class RetrievalChallenge:
    case_id: str
    question: str
    challenge_type: str
    expected_evidence: tuple[str, ...]
    distractor_evidence: tuple[str, ...]
    difficulty: str


def validate_challenge_payload(payload: object) -> list[RetrievalChallenge]:
    if not isinstance(payload, list) or not payload:
        raise RetrievalChallengeValidationError("challenge set must be a non-empty list")
    result: list[RetrievalChallenge] = []
    ids: set[str] = set()
    for item in payload:
        if not isinstance(item, dict) or set(item) != REQUIRED_FIELDS:
            raise RetrievalChallengeValidationError("challenge case has invalid fields")
        case = RetrievalChallenge(**{
            "case_id": item["case_id"],
            "question": item["question"],
            "challenge_type": item["challenge_type"],
            "expected_evidence": tuple(item["expected_evidence"]),
            "distractor_evidence": tuple(item["distractor_evidence"]),
            "difficulty": item["difficulty"],
        })
        if not case.case_id.strip() or not case.question.strip():
            raise RetrievalChallengeValidationError("case_id and question must not be empty")
        if case.challenge_type not in ALLOWED_TYPES:
            raise RetrievalChallengeValidationError("invalid challenge_type")
        if case.difficulty not in ALLOWED_DIFFICULTIES:
            raise RetrievalChallengeValidationError("invalid difficulty")
        if not case.expected_evidence:
            raise RetrievalChallengeValidationError("expected_evidence must not be empty")
        if not case.distractor_evidence:
            raise RetrievalChallengeValidationError("distractor_evidence must not be empty")
        if set(case.expected_evidence) & set(case.distractor_evidence):
            raise RetrievalChallengeValidationError("expected and distractor evidence must be disjoint")
        if case.case_id in ids:
            raise RetrievalChallengeValidationError("duplicate case_id")
        ids.add(case.case_id)
        result.append(case)
    return result


def assert_challenge_evidence_resolved(
    cases: list[RetrievalChallenge],
    available_chunk_ids: set[str],
) -> None:
    missing: dict[str, list[str]] = {}
    for case in cases:
        unresolved = [
            chunk_id
            for chunk_id in (*case.expected_evidence, *case.distractor_evidence)
            if chunk_id not in available_chunk_ids
        ]
        if unresolved:
            missing[case.case_id] = unresolved
    if missing:
        raise RetrievalChallengeValidationError(
            f"unresolved challenge evidence: {missing}"
        )
