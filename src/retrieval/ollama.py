from __future__ import annotations

import os

import httpx


class OllamaEmbeddingProvider:
    """Local Ollama semantic embedding provider."""

    def __init__(
        self,
        model: str | None = None,
        base_url: str | None = None,
        timeout: float | None = None,
    ):
        self.model = model or os.getenv("OLLAMA_EMBEDDING_MODEL", "nomic-embed-text")
        self.base_url = (
            base_url or os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
        ).rstrip("/")
        self.timeout = timeout or float(os.getenv("OLLAMA_TIMEOUT_SECONDS", "30"))
        self._dimensions: int | None = None

    @property
    def dimensions(self) -> int:
        if self._dimensions is None:
            self._dimensions = len(self.embed("dimension probe"))
        return self._dimensions

    def embed(self, text: str) -> list[float]:
        if not text.strip():
            raise ValueError("text must not be empty")
        try:
            response = httpx.post(
                f"{self.base_url}/api/embed",
                json={"model": self.model, "input": text},
                timeout=self.timeout,
            )
            response.raise_for_status()
            embeddings = response.json()["embeddings"]
            vector = embeddings[0]
        except (httpx.HTTPError, httpx.TimeoutException, KeyError, IndexError, TypeError, ValueError) as exc:
            raise RuntimeError("Ollama embedding failed") from exc
        if not vector:
            raise RuntimeError("Ollama returned an empty embedding")
        return [float(value) for value in vector]
