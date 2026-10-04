"""Deterministic BM25 retrieval for controlled retrieval experiments."""

from __future__ import annotations

import math
import re
from collections import Counter

from src.preprocessing.models import Chunk
from src.retrieval.search import Evidence, EvidenceSet


_TOKEN_RE = re.compile(r"[a-z0-9]+")


def _tokens(text: str) -> list[str]:
    return _TOKEN_RE.findall(text.lower())


class BM25Retriever:
    def __init__(self, chunks: list[Chunk], *, k1: float = 1.5, b: float = 0.75):
        if not chunks:
            raise ValueError("chunks must not be empty")
        if k1 <= 0 or not 0 <= b <= 1:
            raise ValueError("invalid BM25 parameters")
        self.chunks = tuple(chunks)
        self.k1 = k1
        self.b = b
        self._tokens = {c.chunk_id: _tokens(c.text) for c in self.chunks}
        self._lengths = {c.chunk_id: len(self._tokens[c.chunk_id]) for c in self.chunks}
        self._avgdl = sum(self._lengths.values()) / len(self.chunks)
        document_frequency: Counter[str] = Counter()
        for tokens in self._tokens.values():
            document_frequency.update(set(tokens))
        self._idf = {
            token: math.log(1.0 + (len(self.chunks) - frequency + 0.5) / (frequency + 0.5))
            for token, frequency in document_frequency.items()
        }

    def _score(self, query_tokens: list[str], chunk: Chunk) -> float:
        counts = Counter(self._tokens[chunk.chunk_id])
        length = self._lengths[chunk.chunk_id]
        score = 0.0
        for token in query_tokens:
            if token not in counts:
                continue
            frequency = counts[token]
            numerator = frequency * (self.k1 + 1)
            denominator = frequency + self.k1 * (1 - self.b + self.b * length / self._avgdl)
            score += self._idf.get(token, 0.0) * numerator / denominator
        return score

    def retrieve(self, query: str, *, top_k: int = 5) -> EvidenceSet:
        if not query.strip():
            raise ValueError("query must not be empty")
        if top_k <= 0:
            raise ValueError("top_k must be greater than zero")
        query_tokens = _tokens(query)
        scored = [(chunk, self._score(query_tokens, chunk)) for chunk in self.chunks]
        scored.sort(key=lambda item: (-item[1], item[0].chunk_id))
        return EvidenceSet(
            query=query,
            evidence=[
                Evidence(chunk=chunk, score=score, rank=rank)
                for rank, (chunk, score) in enumerate(scored[:top_k], start=1)
            ],
        )
