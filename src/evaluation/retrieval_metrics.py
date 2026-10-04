"""Retrieval evaluation metrics for ClinicalQA-v1."""
from dataclasses import dataclass
from math import log2


@dataclass(frozen=True)
class RetrievalMetrics:
    precision_at_k: float
    recall_at_k: float
    mrr: float
    ndcg: float
    k: int
    retrieved_count: int
    expected_count: int


def _validate(retrieved_ids: list[str], expected_ids: set[str], k: int) -> None:
    if k <= 0:
        raise ValueError("k must be greater than zero")
    if len(retrieved_ids) != len(set(retrieved_ids)):
        raise ValueError("retrieved_ids must not contain duplicates")
    if not expected_ids:
        raise ValueError("expected_ids must not be empty")


def precision_at_k(retrieved_ids: list[str], expected_ids: set[str], k: int) -> float:
    _validate(retrieved_ids, expected_ids, k)
    window = retrieved_ids[:k]
    return sum(item in expected_ids for item in window) / k


def recall_at_k(retrieved_ids: list[str], expected_ids: set[str], k: int) -> float:
    _validate(retrieved_ids, expected_ids, k)
    window = retrieved_ids[:k]
    return sum(item in expected_ids for item in window) / len(expected_ids)


def reciprocal_rank(retrieved_ids: list[str], expected_ids: set[str], k: int | None = None) -> float:
    if k is None:
        k = len(retrieved_ids) or 1
    _validate(retrieved_ids, expected_ids, k)
    for rank, item in enumerate(retrieved_ids[:k], start=1):
        if item in expected_ids:
            return 1.0 / rank
    return 0.0


def ndcg_at_k(retrieved_ids: list[str], expected_ids: set[str], k: int) -> float:
    _validate(retrieved_ids, expected_ids, k)
    window = retrieved_ids[:k]
    dcg = sum(
        1.0 / log2(rank + 1)
        for rank, item in enumerate(window, start=1)
        if item in expected_ids
    )
    ideal_hits = min(len(expected_ids), k)
    idcg = sum(1.0 / log2(rank + 1) for rank in range(1, ideal_hits + 1))
    return dcg / idcg if idcg else 0.0


def evaluate_retrieval(
    retrieved_ids: list[str],
    expected_ids: set[str],
    *,
    k: int,
) -> RetrievalMetrics:
    _validate(retrieved_ids, expected_ids, k)
    return RetrievalMetrics(
        precision_at_k=precision_at_k(retrieved_ids, expected_ids, k),
        recall_at_k=recall_at_k(retrieved_ids, expected_ids, k),
        mrr=reciprocal_rank(retrieved_ids, expected_ids, k),
        ndcg=ndcg_at_k(retrieved_ids, expected_ids, k),
        k=k,
        retrieved_count=min(len(retrieved_ids), k),
        expected_count=len(expected_ids),
    )
