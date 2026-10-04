from __future__ import annotations

from sqlalchemy import text
from sqlalchemy.orm import Session

from src.preprocessing.models import Chunk
from .provider import EmbeddingProvider
from .search import Evidence, EvidenceSet


class PgVectorRetriever:
    """Production retrieval adapter using PostgreSQL/pgvector."""

    def __init__(self, session: Session, embedder: EmbeddingProvider, *, column: str = "embedding"):
        if not column.replace("_", "").isalnum():
            raise ValueError("invalid embedding column")
        self.session = session
        self.embedder = embedder
        self.column = column

    def retrieve(self, query: str, *, top_k: int = 5) -> EvidenceSet:
        if not query.strip():
            raise ValueError("query must not be empty")
        if top_k <= 0:
            raise ValueError("top_k must be greater than zero")
        vector = self.embedder.embed(query)
        vector_literal = "[" + ",".join(str(v) for v in vector) + "]"
        try:
            query_sql = f"""
                SELECT chunk_id, document_id, text, section, page, chunk_index,
                       1 - ({self.column} <=> CAST(:query_vector AS vector)) AS score
                FROM chunks
                WHERE {self.column} IS NOT NULL
                ORDER BY {self.column} <=> CAST(:query_vector AS vector), chunk_id
                LIMIT :top_k
            """
            rows = self.session.execute(
                text(query_sql),
                {"query_vector": vector_literal, "top_k": top_k},
            ).mappings().all()
        except Exception as exc:
            raise RuntimeError("pgvector retrieval failed") from exc
        evidence = []
        for rank, row in enumerate(rows, start=1):
            chunk = Chunk(
                row["chunk_id"],
                row["document_id"],
                row["text"],
                row["section"],
                row["page"],
                row["chunk_index"],
            )
            evidence.append(Evidence(chunk=chunk, score=float(row["score"]), rank=rank))
        return EvidenceSet(query=query, evidence=evidence)
