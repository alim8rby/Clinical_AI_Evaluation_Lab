"""Evidence Explorer 2.0 domain models and deterministic trace assembly."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ExplorerCitation:
    citation_id: str
    claim_index: int
    chunk_id: str
    citation_text: str


@dataclass(frozen=True)
class ExplorerClaim:
    claim_index: int
    text: str
    citation_indices: tuple[int, ...]
    citations: tuple[ExplorerCitation, ...]


@dataclass(frozen=True)
class ExplorerChunk:
    chunk_id: str
    document_id: str
    text: str
    section: str | None
    page: int | None
    rank: int
    score: float | None
    used_in_citation: bool


@dataclass(frozen=True)
class ExplorerDocument:
    document_id: str
    title: str
    source: str
    organization: str
    publication_date: str | None
    url: str


@dataclass(frozen=True)
class EvidenceExplorer:
    run_id: str
    question_id: str
    question: str | None
    answer_id: str | None
    answer_text: str | None
    uncertainty: str | None
    claims: tuple[ExplorerClaim, ...]
    chunks: tuple[ExplorerChunk, ...]
    documents: tuple[ExplorerDocument, ...]


def build_explorer(
    *,
    run_id: str,
    question_id: str,
    question: str | None,
    answer_id: str | None,
    answer_text: str | None,
    uncertainty: str | None,
    raw_claims: list[dict] | None,
    citations: list[ExplorerCitation],
    chunks: list[ExplorerChunk],
    documents: list[ExplorerDocument],
) -> EvidenceExplorer:
    citation_by_index: dict[int, list[ExplorerCitation]] = {}
    for citation in citations:
        citation_by_index.setdefault(citation.claim_index, []).append(citation)

    claims = tuple(
        ExplorerClaim(
            claim_index=index,
            text=str(item.get("text", "")),
            citation_indices=tuple(int(value) for value in item.get("citation_indices", [])),
            citations=tuple(citation_by_index.get(index, [])),
        )
        for index, item in enumerate(raw_claims or [])
    )
    used_chunk_ids = {citation.chunk_id for citation in citations}
    normalized_chunks = tuple(
        ExplorerChunk(
            chunk_id=item.chunk_id,
            document_id=item.document_id,
            text=item.text,
            section=item.section,
            page=item.page,
            rank=item.rank,
            score=item.score,
            used_in_citation=item.chunk_id in used_chunk_ids,
        )
        for item in sorted(chunks, key=lambda value: (value.rank, value.chunk_id))
    )
    normalized_documents = tuple(
        sorted(documents, key=lambda value: value.document_id)
    )
    return EvidenceExplorer(
        run_id=run_id,
        question_id=question_id,
        question=question,
        answer_id=answer_id,
        answer_text=answer_text,
        uncertainty=uncertainty,
        claims=claims,
        chunks=normalized_chunks,
        documents=normalized_documents,
    )
