"""Hybrid dense/BM25 retrieval for controlled research experiments."""

from __future__ import annotations

from src.preprocessing.models import Chunk
from src.retrieval.search import Evidence, EvidenceSet, _cosine
from src.retrieval.provider import EmbeddingProvider
from src.retrieval.embeddings import embed_text
from .bm25 import BM25Retriever


class HybridRetriever:
    def __init__(
        self,
        chunks: list[Chunk],
        *,
        embedder: EmbeddingProvider | None = None,
        dense_dimensions: int = 256,
        alpha: float = 0.5,
    ):
        if not chunks:
            raise ValueError("chunks must not be empty")
        if not 0.0 <= alpha <= 1.0:
            raise ValueError("alpha must be between 0 and 1")
        self.chunks = tuple(chunks)
        self.embedder = embedder
        self.dense_dimensions = dense_dimensions
        self.alpha = alpha
        self.bm25 = BM25Retriever(chunks)

    def retrieve(self, query: str, *, top_k: int = 5) -> EvidenceSet:
        if not query.strip():
            raise ValueError("query must not be empty")
        if top_k <= 0:
            raise ValueError("top_k must be greater than zero")

        if self.embedder is None:
            query_vector = embed_text(query, dimensions=self.dense_dimensions)
            dense_vectors = {
                chunk.chunk_id: embed_text(chunk.text, dimensions=self.dense_dimensions)
                for chunk in self.chunks
            }
        else:
            query_vector = self.embedder.embed(query)
            dense_vectors = {
                chunk.chunk_id: self.embedder.embed(chunk.text)
                for chunk in self.chunks
            }

        dense_scores = {
            chunk.chunk_id: _cosine(query_vector, dense_vectors[chunk.chunk_id])
            for chunk in self.chunks
        }
        lexical = self.bm25.retrieve(query, top_k=len(self.chunks))
        lexical_scores = {item.chunk.chunk_id: item.score for item in lexical.evidence}

        dense_max = max(dense_scores.values(), default=0.0)
        lexical_max = max(lexical_scores.values(), default=0.0)

        def normalize(value: float, maximum: float) -> float:
            return value / maximum if maximum > 0 else 0.0

        scored = [
            (
                chunk,
                self.alpha * normalize(dense_scores[chunk.chunk_id], dense_max)
                + (1 - self.alpha) * normalize(lexical_scores.get(chunk.chunk_id, 0.0), lexical_max),
            )
            for chunk in self.chunks
        ]
        scored.sort(key=lambda item: (-item[1], item[0].chunk_id))
        return EvidenceSet(
            query=query,
            evidence=[
                Evidence(chunk=chunk, score=score, rank=rank)
                for rank, (chunk, score) in enumerate(scored[:top_k], start=1)
            ],
        )
