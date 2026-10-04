from src.pipeline import ClinicalRAG
from src.failure_analysis import FailureQuery, FailureObservatory

from app.backend.schemas import (
    CitationResponse,
    EvidenceResponse,
    FailureResponse,
    FailureSummaryResponse,
    QAResponse,
)


def run_qa(rag: ClinicalRAG, question: str, top_k: int) -> QAResponse:
    result = rag.ask(question, top_k=top_k)
    evidence = [
        EvidenceResponse(
            chunk_id=item.chunk.chunk_id,
            document_id=item.chunk.document_id,
            score=item.score,
            rank=item.rank,
            text=item.chunk.text,
        )
        for item in result.evidence.evidence
    ]
    citations = [
        CitationResponse(
            citation_id=item.citation_id,
            answer_id=item.answer_id,
            claim_index=item.claim_index,
            chunk_id=item.chunk_id,
            citation_text=item.citation_text,
        )
        for item in result.citations
    ]
    return QAResponse(
        question=result.question,
        answer=result.answer.answer_text,
        uncertainty=result.answer.uncertainty,
        model=result.answer.model,
        prompt_version=result.answer.prompt_version,
        evidence=evidence,
        citations=citations,
    )


def failure_response(failure) -> FailureResponse:
    return FailureResponse(
        failure_id=failure.failure_id,
        run_id=failure.run_id,
        question_id=failure.question_id,
        category=failure.category,
        type=failure.type,
        severity=failure.severity.value,
        description=failure.description,
        evidence=failure.evidence,
        answer_id=failure.answer_id,
        metric=failure.metric,
        metric_value=failure.metric_value,
        classifier_version=failure.classifier_version,
        created_at=failure.created_at.isoformat() if failure.created_at else None,
    )


def list_failures(observatory: FailureObservatory, query: FailureQuery) -> list[FailureResponse]:
    return [failure_response(item) for item in observatory.list_failures(query)]


def summarize_failures(observatory: FailureObservatory, query: FailureQuery) -> FailureSummaryResponse:
    summary = observatory.summary(query)
    return FailureSummaryResponse(
        total=summary.total,
        by_category=summary.by_category,
        by_type=summary.by_type,
        by_severity=summary.by_severity,
    )
