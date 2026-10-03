from __future__ import annotations
import hashlib
import re
from src.ingestion.models import SourceDocument
from .models import Chunk

class PreprocessingError(ValueError):
    """Raised when preprocessing input is invalid."""

def _clean_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

def _chunk_id(document_id: str, index: int, text: str) -> str:
    raw = f"{document_id}|{index}|{text}"
    return "chunk_" + hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]

def chunk_document(document: SourceDocument, *, max_chars: int = 1200) -> list[Chunk]:
    if max_chars <= 0:
        raise PreprocessingError("max_chars must be greater than zero")
    content = _clean_text(document.content)
    if not content:
        raise PreprocessingError("document content must not be empty")

    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", content) if p.strip()]
    segments: list[str] = []

    for paragraph in paragraphs:
        if len(paragraph) <= max_chars:
            segments.append(paragraph)
            continue

        sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", paragraph) if s.strip()]
        current = ""
        for sentence in sentences:
            if len(sentence) > max_chars:
                if current:
                    segments.append(current)
                    current = ""
                segments.extend(
                    sentence[start:start + max_chars].strip()
                    for start in range(0, len(sentence), max_chars)
                )
            elif not current:
                current = sentence
            elif len(current) + 1 + len(sentence) <= max_chars:
                current = f"{current} {sentence}"
            else:
                segments.append(current)
                current = sentence
        if current:
            segments.append(current)

    return [
        Chunk(
            chunk_id=_chunk_id(document.document_id, index, text),
            document_id=document.document_id,
            text=text,
            section=None,
            page=None,
            chunk_index=index,
        )
        for index, text in enumerate(segments)
    ]
