from pydantic import BaseModel, Field

class ErrorBody(BaseModel): code:str; message:str; details:dict=Field(default_factory=dict)
class ErrorResponse(BaseModel): error:ErrorBody
class HealthResponse(BaseModel): status:str; environment:str; version:str
class QARequest(BaseModel): question:str=Field(min_length=1); top_k:int=Field(default=5,gt=0)
class CitationResponse(BaseModel): citation_id:str; answer_id:str; claim_index:int; chunk_id:str; citation_text:str
class EvidenceResponse(BaseModel): chunk_id:str; document_id:str; score:float; rank:int; text:str
class QAResponse(BaseModel): question:str; answer:str; uncertainty:str|None; model:str; prompt_version:str; evidence:list[EvidenceResponse]; citations:list[CitationResponse]
class FailureResponse(BaseModel):
    failure_id:str; run_id:str; question_id:str; category:str; type:str; severity:str; description:str; evidence:str; answer_id:str|None=None; metric:str|None=None; metric_value:float|None=None; classifier_version:str; created_at:str|None=None
class FailureListResponse(BaseModel): failures:list[FailureResponse]
class FailureSummaryResponse(BaseModel): total:int; by_category:dict[str,int]; by_type:dict[str,int]; by_severity:dict[str,int]
class ExperimentCreateRequest(BaseModel):
    name:str=Field(min_length=1); description:str=""; model_config:dict=Field(default_factory=dict); embedding_config:dict=Field(default_factory=dict); retriever_config:dict=Field(default_factory=dict); top_k:int=Field(default=5,gt=0); prompt_version:str=Field(min_length=1); benchmark_version:str=Field(min_length=1)
class ExperimentResponse(BaseModel):
    experiment_id:str; name:str; description:str; model_config:dict; embedding_config:dict; retriever_config:dict; top_k:int; prompt_version:str; benchmark_version:str; created_at:str
    @classmethod
    def from_domain(cls,e): return cls(experiment_id=e.experiment_id,name=e.name,description=e.description,model_config=e.config.model_config,embedding_config=e.config.embedding_config,retriever_config=e.config.retriever_config,top_k=e.config.top_k,prompt_version=e.config.prompt_version,benchmark_version=e.config.benchmark_version,created_at=e.created_at.isoformat())
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

class ReportResponse(BaseModel):
    experiment_id:str
    benchmark_version:str
    sample_count:int
    configuration:dict
    metrics:dict[str,float]
    failures:list[dict]

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
