from dataclasses import dataclass

from src.retrieval.search import EvidenceSet
from .models import Answer


class CitationError(ValueError):
    """Raised when an answer contains an invalid evidence reference."""


@dataclass(frozen=True)
class Citation:
    citation_id: str
    answer_id: str
    claim_index: int
    chunk_id: str
    citation_text: str


def build_citations(answer: Answer, evidence: EvidenceSet, *, answer_id: str) -> list[Citation]:
    citations: list[Citation] = []
    chunks = {item.chunk.chunk_id: item.chunk for item in evidence.evidence}

    for claim_index, claim in enumerate(answer.claims):
        if not claim.citation_indices:
            raise CitationError(f"claim {claim_index} has no citations")

        for citation_index in claim.citation_indices:
            if citation_index < 1 or citation_index > len(evidence.evidence):
                raise CitationError(
                    f"claim {claim_index} references unavailable evidence index {citation_index}"
                )
            chunk = evidence.evidence[citation_index - 1].chunk
            if chunk.chunk_id not in chunks:
                raise CitationError("citation chunk is not present in the evidence set")
            citations.append(
                Citation(
                    citation_id=f"{answer_id}-c{claim_index}-e{citation_index}",
                    answer_id=answer_id,
                    claim_index=claim_index,
                    chunk_id=chunk.chunk_id,
                    citation_text=f"{chunk.title if hasattr(chunk, 'title') else chunk.chunk_id}",
                )
            )
    return citations
