from __future__ import annotations
from typing import Protocol

class EmbeddingProvider(Protocol):
    dimensions: int
    def embed(self, text: str) -> list[float]:
        """Return an embedding vector for one non-empty text."""

class LocalHashedEmbeddingProvider:
    """Development provider preserving the V1 deterministic embedding baseline."""
    def __init__(self, dimensions: int = 256):
        if dimensions <= 0:
            raise ValueError("dimensions must be greater than zero")
        self.dimensions = dimensions

    def embed(self, text: str) -> list[float]:
        from .embeddings import embed_text
        return embed_text(text, dimensions=self.dimensions)
