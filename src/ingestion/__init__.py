"""Document ingestion package."""

from .ingest import IngestionError, ingest_document, ingest_text_file, make_document_id
from .models import IngestionResult, SourceDocument

__all__ = [
    "IngestionError",
    "IngestionResult",
    "SourceDocument",
    "ingest_document",
    "ingest_text_file",
    "make_document_id",
]
