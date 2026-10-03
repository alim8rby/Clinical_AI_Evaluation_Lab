"""Domain models for document ingestion."""

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class SourceDocument:
    """Normalized source document metadata and content."""

    document_id: str
    title: str
    source: str
    organization: str
    publication_date: date | None
    url: str
    content: str


@dataclass(frozen=True)
class IngestionResult:
    """Result of ingesting one source document."""

    document: SourceDocument
    source_path: str | None = None
