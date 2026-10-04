from fastapi import APIRouter, HTTPException, Query

from app.backend.adapters import list_failures, run_qa, summarize_failures
from app.backend.schemas import (
    FailureListResponse,
    FailureResponse,
    FailureSummaryResponse,
    HealthResponse,
    QARequest,
    QAResponse,
)
from app.backend.services import services
from src.failure_analysis import FailureNotFoundError, FailureQuery

from app.backend.settings import settings

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", environment=settings.app_env, version="0.4.0")


@router.post("/qa", response_model=QAResponse)
def qa(request: QARequest) -> QAResponse:
    if services.rag is None:
        raise HTTPException(status_code=503, detail="QA service is not configured")
    return run_qa(services.rag, request.question, request.top_k)


@router.get("/failures", response_model=FailureListResponse)
def failures(
    category: str | None = None,
    failure_type: str | None = None,
    severity: str | None = None,
    run_id: str | None = None,
    question_id: str | None = None,
    limit: int | None = Query(default=None, gt=0),
) -> FailureListResponse:
    query = FailureQuery(
        category=category,
        failure_type=failure_type,
        severity=severity,
        run_id=run_id,
        question_id=question_id,
        limit=limit,
    )
    return FailureListResponse(failures=list_failures(services.observatory, query))


@router.get("/failures/summary", response_model=FailureSummaryResponse)
def failure_summary(
    category: str | None = None,
    failure_type: str | None = None,
    severity: str | None = None,
    run_id: str | None = None,
    question_id: str | None = None,
) -> FailureSummaryResponse:
    query = FailureQuery(
        category=category,
        failure_type=failure_type,
        severity=severity,
        run_id=run_id,
        question_id=question_id,
    )
    return summarize_failures(services.observatory, query)


@router.get("/failures/{failure_id}", response_model=FailureResponse)
def failure_detail(failure_id: str) -> FailureResponse:
    try:
        failure = services.observatory.get_failure(failure_id)
    except FailureNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    from app.backend.adapters import failure_response
    return failure_response(failure)
