from sqlalchemy import select
from sqlalchemy.orm import Session

from app.backend.db_models import AnswerRow, CitationRow, ChunkRow, DocumentRow, EvaluationRow, ExperimentRow, FailureRow, RunRow
from src.failure_analysis.models import Failure, FailureSeverity
from src.ingestion.models import SourceDocument
from src.preprocessing.models import Chunk
from src.experiments.models import Experiment, ExperimentConfig, RunRecord

class FailureRepository:
    def __init__(self, session: Session): self.session = session
    def save(self, failure):
        existing=self.session.get(FailureRow,failure.failure_id)
        if existing is not None:
            if self._to_domain(existing)!=failure: raise ValueError(f"failure_id already exists with different content: {failure.failure_id}")
            return
        self.session.add(self._to_row(failure)); self.session.commit()
    def save_many(self, failures):
        for failure in failures:
            existing=self.session.get(FailureRow,failure.failure_id)
            if existing is not None and self._to_domain(existing)!=failure: raise ValueError(f"failure_id already exists with different content: {failure.failure_id}")
            if existing is None: self.session.add(self._to_row(failure))
        self.session.commit()
    def get(self,failure_id):
        row=self.session.get(FailureRow,failure_id); return self._to_domain(row) if row else None
    def list(self):
        return [self._to_domain(r) for r in self.session.scalars(select(FailureRow).order_by(FailureRow.failure_id)).all()]
    def count(self): return len(self.list())
    @staticmethod
    def _to_row(f):
        return FailureRow(failure_id=f.failure_id,run_id=f.run_id,question_id=f.question_id,answer_id=f.answer_id,category=f.category,type=f.type,severity=f.severity.value,description=f.description,evidence=f.evidence,metric=f.metric,metric_value=f.metric_value,classifier_version=f.classifier_version,created_at=f.created_at)
    @staticmethod
    def _to_domain(r):
        return Failure(failure_id=r.failure_id,run_id=r.run_id,question_id=r.question_id,category=r.category,type=r.type,severity=FailureSeverity(r.severity),description=r.description,evidence=r.evidence,answer_id=r.answer_id,metric=r.metric,metric_value=r.metric_value,classifier_version=r.classifier_version,created_at=r.created_at)

class ExperimentRepository:
    def __init__(self,session): self.session=session
    def save(self,e):
        self.session.merge(ExperimentRow(experiment_id=e.experiment_id,name=e.name,description=e.description,model_config=e.config.model_config,embedding_config=e.config.embedding_config,retriever_config=e.config.retriever_config,top_k=e.config.top_k,prompt_version=e.config.prompt_version,benchmark_version=e.config.benchmark_version,created_at=e.created_at)); self.session.commit()
    def get(self,eid):
        r=self.session.get(ExperimentRow,eid)
        if not r:return None
        c=ExperimentConfig(r.model_config,r.embedding_config,r.retriever_config,r.top_k,r.prompt_version,r.benchmark_version)
        return Experiment(r.experiment_id,r.name,r.description,c,r.created_at)

class RunRepository:
    def __init__(self,session): self.session=session
    def save(self,run):
        self.session.merge(RunRow(run_id=run.run_id,experiment_id=run.experiment_id,question_id=run.question_id,status=run.status,started_at=run.started_at,finished_at=run.finished_at,latency_ms=run.latency_ms,input_tokens=run.input_tokens,output_tokens=run.output_tokens,cost=run.cost,error=run.error)); self.session.commit()
    def get(self,rid):
        r=self.session.get(RunRow,rid)
        return None if r is None else RunRecord(r.run_id,r.experiment_id,r.question_id,r.status,r.started_at,r.finished_at,r.latency_ms,r.input_tokens,r.output_tokens,r.cost,r.error)

class AnswerRepository:
    def __init__(self,session): self.session=session
    def save(self,answer_id,run_id,answer):
        self.session.merge(AnswerRow(answer_id=answer_id,run_id=run_id,answer_text=answer.answer_text,claims=[{"text":c.text,"citation_indices":list(c.citation_indices)} for c in answer.claims],uncertainty=answer.uncertainty,model=answer.model,prompt_version=answer.prompt_version)); self.session.commit()

class CitationRepository:
    def __init__(self,session): self.session=session
    def save_many(self,citations):
        for c in citations:self.session.merge(CitationRow(citation_id=c.citation_id,answer_id=c.answer_id,claim_index=c.claim_index,chunk_id=c.chunk_id,citation_text=c.citation_text))
        self.session.commit()

class EvaluationRepository:
    def __init__(self,session): self.session=session
    def save(self,evaluation_id,answer_id,evaluator_version,scores,details):
        self.session.merge(EvaluationRow(evaluation_id=evaluation_id,answer_id=answer_id,evaluator_version=evaluator_version,scores=scores,details=details)); self.session.commit()

class DocumentRepository:
    def __init__(self,session): self.session=session
    def save(self,d):
        self.session.merge(DocumentRow(document_id=d.document_id,title=d.title,source=d.source,organization=d.organization,publication_date=d.publication_date,url=d.url,content=d.content)); self.session.commit()
    def get(self,did):
        r=self.session.get(DocumentRow,did)
        return None if r is None else SourceDocument(r.document_id,r.title,r.source,r.organization,r.publication_date,r.url,r.content)

class ChunkRepository:
    def __init__(self,session): self.session=session
    def save_many(self,chunks):
        for c in chunks:self.session.merge(ChunkRow(chunk_id=c.chunk_id,document_id=c.document_id,text=c.text,section=c.section,page=c.page,chunk_index=c.chunk_index))
        self.session.commit()
    def list_by_document(self,did):
        rows=self.session.scalars(select(ChunkRow).where(ChunkRow.document_id==did).order_by(ChunkRow.chunk_index,ChunkRow.chunk_id)).all()
        return [Chunk(r.chunk_id,r.document_id,r.text,r.section,r.page,r.chunk_index) for r in rows]


class ChunkEmbeddingRepository:
    def __init__(self, session: Session):
        self.session = session

    def save_many(self, chunks, embeddings):
        if len(chunks) != len(embeddings):
            raise ValueError("chunks and embeddings must have the same length")
        from sqlalchemy import text

        for chunk, embedding in zip(chunks, embeddings):
            vector_literal = "[" + ",".join(str(float(value)) for value in embedding) + "]"
            self.session.execute(
                text(
                    "UPDATE chunks SET embedding = CAST(:embedding AS vector) "
                    "WHERE chunk_id = :chunk_id"
                ),
                {"embedding": vector_literal, "chunk_id": chunk.chunk_id},
            )
        self.session.commit()


class EvaluationAnalysisRepository:
    def __init__(self, session): self.session=session

    def metric_averages(self, experiment_id):
        rows=self.session.execute(
            select(EvaluationRow, RunRow)
            .join(AnswerRow, AnswerRow.answer_id==EvaluationRow.answer_id)
            .join(RunRow, RunRow.run_id==AnswerRow.run_id)
            .where(RunRow.experiment_id==experiment_id)
        ).all()
        values={}
        for evaluation, run in rows:
            for name,value in (evaluation.scores or {}).items():
                if isinstance(value,(int,float)):
                    values.setdefault(name,[]).append(float(value))
        return {name:sum(items)/len(items) for name,items in sorted(values.items()) if items}

    def completed_run_count(self, experiment_id):
        return len(self.session.execute(
            select(RunRow.run_id).where(RunRow.experiment_id==experiment_id, RunRow.status=="completed")
        ).all())


class RunEvidenceRepository:
    def __init__(self, session): self.session=session

    def get_detail(self, run_id):
        run=self.session.get(RunRow,run_id)
        if run is None: return None
        answer=self.session.scalars(select(AnswerRow).where(AnswerRow.run_id==run_id)).first()
        citations=[]
        if answer is not None:
            citations=self.session.scalars(select(CitationRow).where(CitationRow.answer_id==answer.answer_id).order_by(CitationRow.claim_index,CitationRow.citation_id)).all()
        return run,answer,citations

    def get_evidence(self, run_id):
        bundle=self.get_detail(run_id)
        if bundle is None: return None
        run,answer,citations=bundle
        chunk_ids=sorted({c.chunk_id for c in citations})
        chunks=[]
        for chunk_id in chunk_ids:
            row=self.session.get(ChunkRow,chunk_id)
            if row is not None: chunks.append(row)
        return run,answer,chunks


    def failures_for_experiment(self, experiment_id):
        rows=self.session.execute(
            select(FailureRow).join(RunRow,RunRow.run_id==FailureRow.run_id)
            .where(RunRow.experiment_id==experiment_id)
            .order_by(FailureRow.failure_id)
        ).scalars().all()
        return [FailureRepository._to_domain(row) for row in rows]


class OperationalMetricsRepository:
    def __init__(self, session): self.session=session

    def snapshot(self):
        rows=self.session.scalars(select(RunRow)).all()
        latencies=[float(r.latency_ms) for r in rows if r.latency_ms is not None]
        return {
            "runs_total":len(rows),
            "runs_completed":sum(r.status=="completed" for r in rows),
            "runs_failed":sum(r.status=="failed" for r in rows),
            "failures_total":self.session.query(FailureRow).count(),
            "average_latency_ms":(sum(latencies)/len(latencies)) if latencies else None,
            "input_tokens_total":sum(r.input_tokens or 0 for r in rows),
            "output_tokens_total":sum(r.output_tokens or 0 for r in rows),
            "cost_total":sum(r.cost or 0.0 for r in rows),
        }
