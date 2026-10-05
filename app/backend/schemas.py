from pydantic import BaseModel, Field, ConfigDict

class ErrorBody(BaseModel): code:str; message:str; details:dict=Field(default_factory=dict)
class ErrorResponse(BaseModel): error:ErrorBody
class HealthResponse(BaseModel): status:str; environment:str; version:str
class QARequest(BaseModel): question:str=Field(min_length=1); top_k:int=Field(default=5,gt=0)
class CitationResponse(BaseModel): citation_id:str; answer_id:str; claim_index:int; chunk_id:str; citation_text:str
class EvidenceResponse(BaseModel): chunk_id:str; document_id:str; score:float|None; rank:int; text:str
class QAResponse(BaseModel): question:str; answer:str; uncertainty:str|None; model:str; prompt_version:str; evidence:list[EvidenceResponse]; citations:list[CitationResponse]
class ExplorerCitationResponse(BaseModel):
    citation_id: str
    claim_index: int
    chunk_id: str
    citation_text: str


class ExplorerClaimResponse(BaseModel):
    claim_index: int
    text: str
    citation_indices: list[int]
    citations: list[ExplorerCitationResponse]


class ExplorerChunkResponse(BaseModel):
    chunk_id: str
    document_id: str
    text: str
    section: str | None
    page: int | None
    rank: int
    score: float | None
    used_in_citation: bool


class ExplorerDocumentResponse(BaseModel):
    document_id: str
    title: str
    source: str
    organization: str
    publication_date: str | None
    url: str


class EvidenceExplorerResponse(BaseModel):
    run_id: str
    question_id: str
    question: str | None
    answer_id: str | None
    answer: str | None
    uncertainty: str | None
    claims: list[ExplorerClaimResponse]
    chunks: list[ExplorerChunkResponse]
    documents: list[ExplorerDocumentResponse]


class FailureResponse(BaseModel):
    failure_id:str; run_id:str; question_id:str; category:str; type:str; severity:str; description:str; evidence:str; answer_id:str|None=None; metric:str|None=None; metric_value:float|None=None; classifier_version:str; created_at:str|None=None
class FailureListResponse(BaseModel): failures:list[FailureResponse]
class FailureSummaryResponse(BaseModel): total:int; by_category:dict[str,int]; by_type:dict[str,int]; by_severity:dict[str,int]

class FailureDimensionResponse(BaseModel):
    dimension:str
    value:str
    failure_count:int
    unique_questions:int

class FailureRateResponse(BaseModel):
    dimension:str
    value:str
    failure_count:int
    unique_questions:int
    question_count:int
    failure_rate:float

class FailureRateListResponse(BaseModel):
    experiment_id:str
    rates:list[FailureRateResponse]

class FailureRegressionResponse(BaseModel):
    category:str
    failure_type:str
    baseline_rate:float
    candidate_rate:float
    rate_difference:float
    baseline_questions:int
    candidate_questions:int
    regression:bool
    baseline_affected_questions:int
    candidate_affected_questions:int
    question_level_regression:bool

class FailureObservatoryResponse(BaseModel):
    experiment_id:str
    total_failures:int
    unique_questions:int
    completed_questions:int
    by_category:dict[str,int]
    by_type:dict[str,int]
    by_severity:dict[str,int]
    by_difficulty:dict[str,int]
    by_question_type:dict[str,int]

class FailureRegressionListResponse(BaseModel):
    baseline_experiment_id:str
    candidate_experiment_id:str
    threshold:float
    regressions:list[FailureRegressionResponse]

class ExperimentCreateRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    name: str = Field(min_length=1)
    description: str = ""
    model_config_: dict = Field(default_factory=dict, alias="model_config")
    embedding_config: dict = Field(default_factory=dict)
    retriever_config: dict = Field(default_factory=dict)
    top_k: int = Field(default=5, gt=0)
    prompt_version: str = Field(min_length=1)
    benchmark_version: str = Field(min_length=1)
class ExperimentResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    experiment_id: str
    name: str
    description: str
    model_config_: dict = Field(alias="model_config")
    embedding_config: dict
    retriever_config: dict
    top_k: int
    prompt_version: str
    benchmark_version: str
    created_at: str

    @classmethod
    def from_domain(cls, e):
        return cls(
            experiment_id=e.experiment_id,
            name=e.name,
            description=e.description,
            model_config_=e.config.model_config,
            embedding_config=e.config.embedding_config,
            retriever_config=e.config.retriever_config,
            top_k=e.config.top_k,
            prompt_version=e.config.prompt_version,
            benchmark_version=e.config.benchmark_version,
            created_at=e.created_at.isoformat(),
        )
class RunRequest(BaseModel):
    question_id:str=Field(min_length=1); question:str=Field(min_length=1); domain:str="depression"; difficulty:str="easy"; expected_evidence:list[str]=Field(min_length=1); reference_answer:str=Field(min_length=1); key_concepts:list[str]=Field(min_length=1)
class RunResponse(BaseModel):
    run_id:str; experiment_id:str; question_id:str; status:str; started_at:str; finished_at:str|None; latency_ms:float|None; input_tokens:int|None; output_tokens:int|None; cost:float|None; error:str|None
    @classmethod
    def from_run(cls,r): return cls(run_id=r.run_id,experiment_id=r.experiment_id,question_id=r.question_id,status=r.status,started_at=r.started_at.isoformat(),finished_at=r.finished_at.isoformat() if r.finished_at else None,latency_ms=r.latency_ms,input_tokens=r.input_tokens,output_tokens=r.output_tokens,cost=r.cost,error=r.error)
    @classmethod
    def from_result(cls,r): return cls.from_run(r.run)

class ComparisonRequest(BaseModel):
    baseline_experiment_id:str=Field(min_length=1)
    candidate_experiment_id:str=Field(min_length=1)

class MetricDeltaResponse(BaseModel):
    metric:str
    baseline:float
    candidate:float
    delta:float

class ComparisonResponse(BaseModel):
    baseline_experiment_id:str
    candidate_experiment_id:str
    benchmark_version:str
    metric_deltas:list[MetricDeltaResponse]


class RunDetailResponse(RunResponse):
    answer_id:str|None=None
    answer:str|None=None
    uncertainty:str|None=None
    model:str|None=None
    prompt_version:str|None=None
    citations:list[CitationResponse]=Field(default_factory=list)

class RunEvidenceResponse(BaseModel):
    run_id:str
    answer_id:str|None=None
    evidence:list[EvidenceResponse]



class ReportResponse(BaseModel):
    experiment_id:str
    benchmark_version:str
    sample_count:int
    configuration:dict
    metrics:dict[str,float]
    failures:list[dict]

class MetricsResponse(BaseModel):
    runs_total:int
    runs_completed:int
    runs_failed:int
    failures_total:int
    average_latency_ms:float|None=None
    input_tokens_total:int
    output_tokens_total:int
    cost_total:float
