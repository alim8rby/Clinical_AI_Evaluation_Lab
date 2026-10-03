from dataclasses import dataclass
from math import sqrt
from pathlib import Path
import json
from src.preprocessing.models import Chunk

@dataclass(frozen=True)
class EmbeddedChunk:
    chunk: Chunk
    vector: list[float]

def embed_text(text: str, *, dimensions: int = 256) -> list[float]:
    if dimensions <= 0:
        raise ValueError("dimensions must be greater than zero")
    tokens = text.lower().split()
    if not tokens:
        raise ValueError("text must not be empty")
    vector = [0.0] * dimensions
    for token in tokens:
        index = sum(token.encode("utf-8")) % dimensions
        vector[index] += 1.0
    norm = sqrt(sum(v * v for v in vector))
    return [v / norm for v in vector]

class VectorIndex:
    def __init__(self, path: str | Path, *, dimensions: int = 256):
        if dimensions <= 0:
            raise ValueError("dimensions must be greater than zero")
        self.path = Path(path)
        self.dimensions = dimensions
        self._items: dict[str, EmbeddedChunk] = {}

    def add(self, chunks: list[Chunk]) -> None:
        for chunk in chunks:
            self._items[chunk.chunk_id] = EmbeddedChunk(chunk, embed_text(chunk.text, dimensions=self.dimensions))

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        items = []
        for item in self._items.values():
            c = item.chunk
            items.append({"chunk_id":c.chunk_id,"document_id":c.document_id,"text":c.text,"section":c.section,"page":c.page,"chunk_index":c.chunk_index,"vector":item.vector})
        self.path.write_text(json.dumps({"dimensions":self.dimensions,"items":items}, indent=2), encoding="utf-8")

    def load(self) -> None:
        payload = json.loads(self.path.read_text(encoding="utf-8"))
        if payload["dimensions"] != self.dimensions:
            raise ValueError("stored index dimensions do not match")
        self._items = {}
        for item in payload["items"]:
            chunk = Chunk(item["chunk_id"], item["document_id"], item["text"], item["section"], item["page"], item["chunk_index"])
            self._items[chunk.chunk_id] = EmbeddedChunk(chunk, item["vector"])

    @property
    def size(self) -> int:
        return len(self._items)
