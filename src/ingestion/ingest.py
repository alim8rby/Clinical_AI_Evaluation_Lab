"""Controlled document ingestion for the V1 knowledge pipeline."""

from __future__ import annotations

import hashlib
import re
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

from .models import IngestionResult, SourceDocument


class IngestionError(ValueError):
    """Raised when a source cannot be normalized into a valid document."""


def _required(value: str, field: str) -> str:
    value = value.strip()
    if not value:
        raise IngestionError(f"{field} must not be empty")
    return value


def _normalize_content(content: str) -> str:
    content = content.replace("\r\n", "\n").replace("\r", "\n")
    content = re.sub(r"[ \t]+", " ", content)
    content = re.sub(r"\n{3,}", "\n\n", content)
    return content.strip()


def _validate_url(url: str) -> str:
    url = _required(url, "url")
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise IngestionError("url must be an absolute HTTP(S) URL")
    return url


def make_document_id(*, title: str, organization: str, url: str) -> str:
    """Create a deterministic identifier from stable source metadata."""
    identity = "|".join(
        (_required(title, "title"), _required(organization, "organization"), _validate_url(url))
    )
    return "doc_" + hashlib.sha256(identity.encode("utf-8")).hexdigest()[:16]


def ingest_document(
    *,
    title: str,
    source: str,
    organization: str,
    publication_date: date | None,
    url: str,
    content: str,
    source_path: str | None = None,
) -> IngestionResult:
    """Validate and normalize one authoritative source document."""
    normalized_content = _normalize_content(content)
    if not normalized_content:
        raise IngestionError("content must not be empty")

    normalized_title = _required(title, "title")
    normalized_source = _required(source, "source")
    normalized_organization = _required(organization, "organization")
    normalized_url = _validate_url(url)

    document = SourceDocument(
        document_id=make_document_id(
            title=normalized_title,
            organization=normalized_organization,
            url=normalized_url,
        ),
        title=normalized_title,
        source=normalized_source,
        organization=normalized_organization,
        publication_date=publication_date,
        url=normalized_url,
        content=normalized_content,
    )
    return IngestionResult(document=document, source_path=source_path)


def ingest_text_file(
    path: str | Path,
    *,
    title: str,
    source: str,
    organization: str,
    publication_date: date | None,
    url: str,
) -> IngestionResult:
    """Read a UTF-8 text source and pass it through the same validation path."""
    file_path = Path(path)
    content = file_path.read_text(encoding="utf-8")
    return ingest_document(
        title=title,
        source=source,
        organization=organization,
        publication_date=publication_date,
        url=url,
        content=content,
        source_path=str(file_path),
    )
