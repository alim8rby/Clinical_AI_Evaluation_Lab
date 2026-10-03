from dataclasses import dataclass
from math import sqrt

from .embeddings import VectorIndex, embed_text
from src.preprocessing.models import Chunk


@dataclass(frozen=True)
class Evidence:
    chunk: Chunk
    score: float
    rank: int


@dataclass(frozen=True)
class EvidenceSet:
    query: str
    evidence: list[Evidence]


def _cosine(left: list[float], right: list[float]) -> float:
    numerator = sum(a * b for a, b in zip(left, right))
    left_norm = sqrt(sum(a * a for a in left))
    right_norm = sqrt(sum(b * b for b in right))
    if not left_norm or not right_norm:
        return 0.0
    return numerator / (left_norm * right_norm)


def retrieve(index: VectorIndex, query: str, *, top_k: int = 5) -> EvidenceSet:
    if not query.strip():
        raise ValueError("query must not be empty")
    if top_k <= 0:
        raise ValueError("top_k must be greater than zero")

    query_vector = embed_text(query, dimensions=index.dimensions)
    scored = [
        (item.chunk, _cosine(query_vector, item.vector))
        for item in index._items.values()
    ]
    scored.sort(key=lambda pair: (-pair[1], pair[0].chunk_id))
    evidence = [
        Evidence(chunk=chunk, score=score, rank=rank)
        for rank, (chunk, score) in enumerate(scored[:top_k], start=1)
    ]
    return EvidenceSet(query=query, evidence=evidence)
