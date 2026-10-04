from pydantic import BaseModel, Field


class ErrorBody(BaseModel):
    code: str
    message: str
    details: dict = Field(default_factory=dict)


class ErrorResponse(BaseModel):
    error: ErrorBody


class HealthResponse(BaseModel):
    status: str
    environment: str
    version: str


class QARequest(BaseModel):
    question: str = Field(min_length=1)
    top_k: int = Field(default=5, gt=0)


class CitationResponse(BaseModel):
    citation_id: str
    answer_id: str
    claim_index: int
    chunk_id: str
    citation_text: str


class EvidenceResponse(BaseModel):
    chunk_id: str
    document_id: str
    score: float
    rank: int
    text: str


class QAResponse(BaseModel):
    question: str
    answer: str
    uncertainty: str | None
    model: str
    prompt_version: str
    evidence: list[EvidenceResponse]
    citations: list[CitationResponse]


class FailureResponse(BaseModel):
    failure_id: str
    run_id: str
    question_id: str
    category: str
    type: str
    severity: str
    description: str
    evidence: str
    answer_id: str | None = None
    metric: str | None = None
    metric_value: float | None = None
    classifier_version: str
    created_at: str | None = None


class FailureListResponse(BaseModel):
    failures: list[FailureResponse]


class FailureSummaryResponse(BaseModel):
    total: int
    by_category: dict[str, int]
    by_type: dict[str, int]
    by_severity: dict[str, int]
