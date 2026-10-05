from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Query
from app.backend.adapters import failure_response, list_failures, run_qa, summarize_failures
from app.backend.repositories import EvaluationAnalysisRepository, RunEvidenceRepository, OperationalMetricsRepository, RunEvidenceExplorerRepository
from app.backend.schemas import *
from app.backend.services import services, DatabaseFailureObservatoryV2
from src.evaluation.benchmark import BenchmarkQuestion
from src.experiments.models import Experiment, ExperimentConfig
from src.failure_analysis import FailureNotFoundError, FailureQuery
from app.backend.settings import settings

router=APIRouter()

@router.get("/health",response_model=HealthResponse)
def health(): return HealthResponse(status="ok",environment=settings.app_env,version="0.4.0")

@router.get("/metrics",response_model=MetricsResponse)
def metrics():
    session=services.session()
    try:
        return MetricsResponse(**OperationalMetricsRepository(session).snapshot())
    finally:
        session.close()

@router.post("/qa",response_model=QAResponse)
def qa(request:QARequest):
    if services.rag is None: raise HTTPException(status_code=503,detail="QA service is not configured")
    return run_qa(services.rag,request.question,request.top_k)

@router.post("/experiments",response_model=ExperimentResponse)
def create_experiment(request:ExperimentCreateRequest):
    config=ExperimentConfig(request.model_config_,request.embedding_config,request.retriever_config,request.top_k,request.prompt_version,request.benchmark_version)
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


@router.get("/failures/experiments/{experiment_id}/analysis",response_model=FailureObservatoryResponse)
def failure_experiment_analysis(experiment_id:str):
    session=services.session()
    try:
        analysis=DatabaseFailureObservatoryV2(services.session).for_experiment(experiment_id)
        return FailureObservatoryResponse(
            experiment_id=analysis.experiment_id,
            total_failures=analysis.total_failures,
            unique_questions=analysis.unique_questions,
            completed_questions=analysis.completed_questions or 0,
            by_category=analysis.by_category,
            by_type=analysis.by_type,
            by_severity=analysis.by_severity,
            by_difficulty=analysis.by_difficulty,
            by_question_type=analysis.by_question_type,
        )
    finally:
        session.close()

@router.get("/failures/experiments/{experiment_id}/rates",response_model=FailureRateListResponse)
def failure_dimension_rates(
    experiment_id:str,
    dimension:str=Query(...,pattern="^(category|type|severity|difficulty|question_type)$"),
):
    session=services.session()
    try:
        runtime=services.runtime(session)
        experiment=runtime.experiments.get(experiment_id)
        if experiment is None:
            raise HTTPException(status_code=404,detail="experiment not found")
        rates=DatabaseFailureObservatoryV2(services.session).rates(experiment_id,dimension)
        return FailureRateListResponse(
            experiment_id=experiment_id,
            rates=[
                FailureRateResponse(
                    dimension=item.dimension,
                    value=item.value,
                    failure_count=item.failure_count,
                    unique_questions=item.unique_questions,
                    question_count=item.question_count,
                    failure_rate=item.failure_rate,
                )
                for item in rates
            ],
        )
    finally:
        session.close()

@router.get("/failures/regression",response_model=FailureRegressionListResponse)
def failure_regression(
    baseline_experiment_id:str,
    candidate_experiment_id:str,
    threshold:float=Query(default=0.10,ge=0.0),
):
    session=services.session()
    try:
        runtime=services.runtime(session)
        baseline=runtime.experiments.get(baseline_experiment_id)
        candidate=runtime.experiments.get(candidate_experiment_id)
        if baseline is None or candidate is None:
            raise HTTPException(status_code=404,detail="experiment not found")
        if baseline.config.benchmark_version != candidate.config.benchmark_version:
            raise HTTPException(status_code=400,detail="experiments must use the same benchmark version")
        if baseline_experiment_id == candidate_experiment_id:
            raise HTTPException(status_code=400,detail="baseline and candidate experiments must differ")
        regressions=DatabaseFailureObservatoryV2(services.session).regression(
            baseline_experiment_id,candidate_experiment_id,threshold
        )
        return FailureRegressionListResponse(
            baseline_experiment_id=baseline_experiment_id,
            candidate_experiment_id=candidate_experiment_id,
            threshold=threshold,
            regressions=[
                FailureRegressionResponse(
                    category=item.category,
                    failure_type=item.failure_type,
                    baseline_rate=item.baseline_rate,
                    candidate_rate=item.candidate_rate,
                    rate_difference=item.rate_difference,
                    baseline_questions=item.baseline_questions,
                    candidate_questions=item.candidate_questions,
                    regression=item.regression,
                    baseline_affected_questions=item.baseline_affected_questions,
                    candidate_affected_questions=item.candidate_affected_questions,
                    question_level_regression=item.question_level_regression,
                )
                for item in regressions
            ],
        )
    finally:
        session.close()

@router.get("/failures/{failure_id}",response_model=FailureResponse)
def failure_detail(failure_id:str):
    try:return failure_response(services.observatory.get_failure(failure_id))
    except FailureNotFoundError as exc: raise HTTPException(status_code=404,detail=str(exc)) from exc

@router.get("/runs/{run_id}/evidence/explorer",response_model=EvidenceExplorerResponse)
def run_evidence_explorer(run_id: str):
    session = services.session()
    try:
        run = services.runtime(session).runs.get(run_id)
        if run is None:
            raise HTTPException(status_code=404, detail="run not found")
        experiment = services.runtime(session).experiments.get(run.experiment_id)
        if experiment is None:
            raise HTTPException(status_code=404, detail="experiment not found")
        explorer = RunEvidenceExplorerRepository(session).get(
            run_id,
            experiment.config.benchmark_version,
        )
        if explorer is None:
            raise HTTPException(status_code=404, detail="evidence trace not found")
        return EvidenceExplorerResponse(
            run_id=explorer.run_id,
            question_id=explorer.question_id,
            question=explorer.question,
            answer_id=explorer.answer_id,
            answer=explorer.answer_text,
            uncertainty=explorer.uncertainty,
            claims=[
                ExplorerClaimResponse(
                    claim_index=item.claim_index,
                    text=item.text,
                    citation_indices=list(item.citation_indices),
                    citations=[
                        ExplorerCitationResponse(
                            citation_id=c.citation_id,
                            claim_index=c.claim_index,
                            chunk_id=c.chunk_id,
                            citation_text=c.citation_text,
                        )
                        for c in item.citations
                    ],
                )
                for item in explorer.claims
            ],
            chunks=[
                ExplorerChunkResponse(
                    chunk_id=item.chunk_id,
                    document_id=item.document_id,
                    text=item.text,
                    section=item.section,
                    page=item.page,
                    rank=item.rank,
                    score=item.score,
                    used_in_citation=item.used_in_citation,
                )
                for item in explorer.chunks
            ],
            documents=[
                ExplorerDocumentResponse(
                    document_id=item.document_id,
                    title=item.title,
                    source=item.source,
                    organization=item.organization,
                    publication_date=item.publication_date,
                    url=item.url,
                )
                for item in explorer.documents
            ],
        )
    finally:
        session.close()


@router.get("/runs/{run_id}/evidence",response_model=RunEvidenceResponse)
def run_evidence(run_id:str):
    session=services.session()
    try:
        bundle=RunEvidenceRepository(session).get_evidence(run_id)
        if bundle is None: raise HTTPException(status_code=404,detail="run not found")
        run,answer,chunks=bundle
        return RunEvidenceResponse(
            run_id=run.run_id,
            answer_id=answer.answer_id if answer else None,
            evidence=[EvidenceResponse(chunk_id=c.chunk_id,document_id=c.document_id,score=None,rank=c.chunk_index+1,text=c.text) for c in chunks],
        )
    finally: session.close()

@router.get("/experiments/{experiment_id}/report",response_model=ReportResponse)
def experiment_report(experiment_id:str):
    session=services.session()
    try:
        runtime=services.runtime(session)
        experiment=runtime.experiments.get(experiment_id)
        if experiment is None: raise HTTPException(status_code=404,detail="experiment not found")
        repo=EvaluationAnalysisRepository(session)
        failures=[failure.to_dict() for failure in repo.failures_for_experiment(experiment_id)]
        return ReportResponse(
            experiment_id=experiment.experiment_id,
            benchmark_version=experiment.config.benchmark_version,
            sample_count=repo.completed_run_count(experiment_id),
            configuration={"model_config":experiment.config.model_config,"embedding_config":experiment.config.embedding_config,"retriever_config":experiment.config.retriever_config,"top_k":experiment.config.top_k,"prompt_version":experiment.config.prompt_version},
            metrics=repo.metric_averages(experiment_id),
            failures=failures,
        )
    finally: session.close()
