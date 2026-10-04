"""Deterministic grounding and citation metrics."""
from dataclasses import dataclass
import re

from src.generation.citations import Citation
from src.generation.models import Answer
from src.retrieval.search import EvidenceSet


@dataclass(frozen=True)
class GroundingMetrics:
    citation_coverage: float
    citation_validity: float
    faithfulness: float
    unsupported_claim_rate: float


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def _support_score(claim_text: str, evidence_text: str) -> float:
    claim = _tokens(claim_text)
    evidence = _tokens(evidence_text)
    if not claim:
        return 0.0
    return len(claim & evidence) / len(claim)


def evaluate_grounding(
    answer: Answer,
    citations: list[Citation],
    evidence: EvidenceSet,
) -> GroundingMetrics:
    claims = answer.claims
    if not claims:
        return GroundingMetrics(0.0, 0.0, 0.0, 1.0)

    evidence_by_id = {item.chunk.chunk_id: item.chunk.text for item in evidence.evidence}
    citations_by_claim: dict[int, list[Citation]] = {}
    for citation in citations:
        citations_by_claim.setdefault(citation.claim_index, []).append(citation)

    covered = 0
    valid = 0
    faithful = 0.0

    for index, claim in enumerate(claims, start=1):
        claim_citations = citations_by_claim.get(index, [])
        if claim_citations:
            covered += 1
        valid_citations = [
            citation for citation in claim_citations
            if citation.chunk_id in evidence_by_id
        ]
        if valid_citations:
            valid += 1
            faithful += max(
                _support_score(claim.text, evidence_by_id[citation.chunk_id])
                for citation in valid_citations
            )

    citation_coverage = covered / len(claims)
    citation_validity = valid / len(claims)
    faithfulness = faithful / len(claims)
    return GroundingMetrics(
        citation_coverage=citation_coverage,
        citation_validity=citation_validity,
        faithfulness=faithfulness,
        unsupported_claim_rate=1.0 - faithfulness,
    )
