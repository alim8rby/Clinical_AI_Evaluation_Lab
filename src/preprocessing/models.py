from dataclasses import dataclass

@dataclass(frozen=True)
class Chunk:
    """A retrievable document segment with preserved provenance."""
    chunk_id: str
    document_id: str
    text: str
    section: str | None
    page: int | None
    chunk_index: int
