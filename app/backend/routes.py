from fastapi import APIRouter, HTTPException, Query
from app.backend.adapters import failure_response, list_failures, run_qa, summarize_failures
from app.backend.repositories import EvaluationAnalysisRepository
from app.backend.schemas import *
from app.backend.services import services
from src.evaluation.benchmark import BenchmarkQuestion
from src.experiments.models import Experiment, ExperimentConfig
from src.failure_analysis import FailureNotFoundError, FailureQuery
from app.backend.settings import settings

router=APIRouter()

@router.get("/health",response_model=HealthResponse)
def health(): return HealthResponse(status="ok",environment=settings.app_env,version="0.4.0")

@router.post("/qa",response_model=QAResponse)
def qa(request:QARequest):
    if services.rag is None: raise HTTPException(status_code=503,detail="QA service is not configured")
    return run_qa(services.rag,request.question,request.top_k)

@router.post("/experiments",response_model=ExperimentResponse)
def create_experiment(request:ExperimentCreateRequest):
    config=ExperimentConfig(request.model_config,request.embedding_config,request.retriever_config,request.top_k,request.prompt_version,request.benchmark_version)
    experiment=Experiment.create(request.name,request.description,config,created_at=datetime.now(timezone.utc).replace(tzinfo=None))
    session=services.session()
    try: services.runtime(session).create_experiment(experiment)
    finally: session.close()
    return ExperimentResponse.from_domain(experiment)

@router.get("/experiments/{experiment_id}",response_model=ExperimentResponse)
def get_experiment(experiment_id:str):
    session=services.session()
    try: experiment=services.runtime(session).experiments.get(experiment_id)
    finally: session.close()
    if experiment is None: raise HTTPException(status_code=404,detail="experiment not found")
    return ExperimentResponse.from_domain(experiment)

@router.post("/experiments/{experiment_id}/runs",response_model=RunResponse)
def run_experiment(experiment_id:str,request:RunRequest):
    session=services.session()
    try:
        runtime=services.runtime(session)
        experiment=runtime.experiments.get(experiment_id)
        if experiment is None: raise HTTPException(status_code=404,detail="experiment not found")
        question=BenchmarkQuestion(request.question_id,request.question,request.domain,request.difficulty,tuple(request.expected_evidence),request.reference_answer,tuple(request.key_concepts))
        return RunResponse.from_result(runtime.run_question(experiment,question).result)
    finally: session.close()

@router.get("/runs/{run_id}",response_model=RunResponse)
def get_run(run_id:str):
    session=services.session()
    try: run=services.runtime(session).runs.get(run_id)
    finally: session.close()
    if run is None: raise HTTPException(status_code=404,detail="run not found")
    return RunResponse.from_run(run)

@router.post("/comparisons",response_model=ComparisonResponse)
def compare(request:ComparisonRequest):
    session=services.session()
    try:
        runtime=services.runtime(session)
        baseline=runtime.experiments.get(request.baseline_experiment_id)
        candidate=runtime.experiments.get(request.candidate_experiment_id)
        if baseline is None or candidate is None: raise HTTPException(status_code=404,detail="experiment not found")
        if baseline.config.benchmark_version != candidate.config.benchmark_version: raise HTTPException(status_code=400,detail="experiments must use the same benchmark version")
        repo=EvaluationAnalysisRepository(session)
        base=repo.metric_averages(baseline.experiment_id)
        cand=repo.metric_averages(candidate.experiment_id)
        shared=sorted(set(base)&set(cand))
        return ComparisonResponse(baseline_experiment_id=baseline.experiment_id,candidate_experiment_id=candidate.experiment_id,benchmark_version=baseline.config.benchmark_version,metric_deltas=[MetricDeltaResponse(metric=k,baseline=base[k],candidate=cand[k],delta=cand[k]-base[k]) for k in shared])
    finally: session.close()

@router.get("/failures",response_model=FailureListResponse)
def failures(category:str|None=None,failure_type:str|None=None,severity:str|None=None,run_id:str|None=None,question_id:str|None=None,limit:int|None=Query(default=None,gt=0)):
    return FailureListResponse(failures=list_failures(services.observatory,FailureQuery(category=category,failure_type=failure_type,severity=severity,run_id=run_id,question_id=question_id,limit=limit)))

@router.get("/failures/summary",response_model=FailureSummaryResponse)
def failure_summary(category:str|None=None,failure_type:str|None=None,severity:str|None=None,run_id:str|None=None,question_id:str|None=None):
    return summarize_failures(services.observatory,FailureQuery(category=category,failure_type=failure_type,severity=severity,run_id=run_id,question_id=question_id))

@router.get("/failures/{failure_id}",response_model=FailureResponse)
def failure_detail(failure_id:str):
    try:return failure_response(services.observatory.get_failure(failure_id))
    except FailureNotFoundError as exc: raise HTTPException(status_code=404,detail=str(exc)) from exc
