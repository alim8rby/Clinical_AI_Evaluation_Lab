"""Benchmark-facing retrieval evaluation."""
from dataclasses import dataclass

from src.evaluation.benchmark import BenchmarkQuestion
from src.evaluation.retrieval_metrics import RetrievalMetrics, evaluate_retrieval
from src.retrieval.search import EvidenceSet


@dataclass(frozen=True)
class RetrievalEvaluation:
    question_id: str
    metrics: RetrievalMetrics
    retrieved_ids: tuple[str, ...]
    expected_ids: tuple[str, ...]


def evaluate_question_retrieval(
    question: BenchmarkQuestion,
    evidence: EvidenceSet,
    *,
    k: int,
) -> RetrievalEvaluation:
    retrieved_ids = [item.chunk.chunk_id for item in evidence.evidence]
    expected_ids = set(question.expected_evidence)
    metrics = evaluate_retrieval(retrieved_ids, expected_ids, k=k)
    return RetrievalEvaluation(
        question_id=question.question_id,
        metrics=metrics,
        retrieved_ids=tuple(retrieved_ids[:k]),
        expected_ids=tuple(sorted(expected_ids)),
    )
