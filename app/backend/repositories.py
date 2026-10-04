from sqlalchemy import select
from sqlalchemy.orm import Session

from app.backend.db_models import FailureRow
from src.failure_analysis.models import Failure, FailureSeverity


class FailureRepository:
    """SQLAlchemy adapter for Failure domain persistence."""

    def __init__(self, session: Session):
        self.session = session

    def save(self, failure: Failure) -> None:
        existing = self.session.get(FailureRow, failure.failure_id)
        if existing is not None:
            if self._to_domain(existing) != failure:
                raise ValueError(
                    f"failure_id already exists with different content: {failure.failure_id}"
                )
            return
        self.session.add(self._to_row(failure))
        self.session.commit()

    def save_many(self, failures: list[Failure] | tuple[Failure, ...]) -> None:
        for failure in failures:
            existing = self.session.get(FailureRow, failure.failure_id)
            if existing is not None and self._to_domain(existing) != failure:
                raise ValueError(
                    f"failure_id already exists with different content: {failure.failure_id}"
                )
            if existing is None:
                self.session.add(self._to_row(failure))
        self.session.commit()

    def get(self, failure_id: str) -> Failure | None:
        row = self.session.get(FailureRow, failure_id)
        return self._to_domain(row) if row else None

    def list(self) -> list[Failure]:
        rows = self.session.scalars(select(FailureRow).order_by(FailureRow.failure_id)).all()
        return [self._to_domain(row) for row in rows]

    def count(self) -> int:
        return len(self.list())

    @staticmethod
    def _to_row(failure: Failure) -> FailureRow:
        return FailureRow(
            failure_id=failure.failure_id,
            run_id=failure.run_id,
            question_id=failure.question_id,
            answer_id=failure.answer_id,
            category=failure.category,
            type=failure.type,
            severity=failure.severity.value,
            description=failure.description,
            evidence=failure.evidence,
            metric=failure.metric,
            metric_value=failure.metric_value,
            classifier_version=failure.classifier_version,
            created_at=failure.created_at,
        )

    @staticmethod
    def _to_domain(row: FailureRow) -> Failure:
        return Failure(
            failure_id=row.failure_id,
            run_id=row.run_id,
            question_id=row.question_id,
            category=row.category,
            type=row.type,
            severity=FailureSeverity(row.severity),
            description=row.description,
            evidence=row.evidence,
            answer_id=row.answer_id,
            metric=row.metric,
            metric_value=row.metric_value,
            classifier_version=row.classifier_version,
            created_at=row.created_at,
        )


from src.ingestion.models import SourceDocument
from src.preprocessing.models import Chunk
from src.experiments.models import Experiment, ExperimentConfig, RunRecord


class DocumentRepository:
    def __init__(self, session: Session):
        self.session = session

    def save(self, document: SourceDocument) -> None:
        self.session.merge(DocumentRow(
            document_id=document.document_id, title=document.title, source=document.source,
            organization=document.organization, publication_date=document.publication_date,
            url=document.url, content=document.content,
        ))
        self.session.commit()

    def get(self, document_id: str) -> SourceDocument | None:
        row = self.session.get(DocumentRow, document_id)
        if row is None:
            return None
        return SourceDocument(row.document_id, row.title, row.source, row.organization,
                              row.publication_date, row.url, row.content)


class ChunkRepository:
    def __init__(self, session: Session):
        self.session = session

    def save_many(self, chunks: list[Chunk] | tuple[Chunk, ...]) -> None:
        for chunk in chunks:
            self.session.merge(ChunkRow(
                chunk_id=chunk.chunk_id, document_id=chunk.document_id, text=chunk.text,
                section=chunk.section, page=chunk.page, chunk_index=chunk.chunk_index,
            ))
        self.session.commit()

    def list_by_document(self, document_id: str) -> list[Chunk]:
        rows = self.session.scalars(
            select(ChunkRow).where(ChunkRow.document_id == document_id)
            .order_by(ChunkRow.chunk_index, ChunkRow.chunk_id)
        ).all()
        return [Chunk(r.chunk_id, r.document_id, r.text, r.section, r.page, r.chunk_index) for r in rows]


class ExperimentRepository:
    def __init__(self, session: Session):
        self.session = session

    def save(self, experiment: Experiment) -> None:
        self.session.merge(ExperimentRow(
            experiment_id=experiment.experiment_id, name=experiment.name,
            description=experiment.description, model_config=experiment.config.model_config,
            embedding_config=experiment.config.embedding_config,
            retriever_config=experiment.config.retriever_config, top_k=experiment.config.top_k,
            prompt_version=experiment.config.prompt_version,
            benchmark_version=experiment.config.benchmark_version,
            created_at=experiment.created_at,
        ))
        self.session.commit()

    def get(self, experiment_id: str) -> Experiment | None:
        row = self.session.get(ExperimentRow, experiment_id)
        if row is None:
            return None
        config = ExperimentConfig(row.model_config, row.embedding_config, row.retriever_config,
                                  row.top_k, row.prompt_version, row.benchmark_version)
        return Experiment(row.experiment_id, row.name, row.description, config, row.created_at)


class RunRepository:
    def __init__(self, session: Session):
        self.session = session

    def save(self, run: RunRecord) -> None:
        self.session.merge(RunRow(
            run_id=run.run_id, experiment_id=run.experiment_id, question_id=run.question_id,
            status=run.status, started_at=run.started_at, finished_at=run.finished_at,
            latency_ms=run.latency_ms, input_tokens=run.input_tokens,
            output_tokens=run.output_tokens, cost=run.cost, error=run.error,
        ))
        self.session.commit()

    def get(self, run_id: str) -> RunRecord | None:
        row = self.session.get(RunRow, run_id)
        if row is None:
            return None
        return RunRecord(row.run_id, row.experiment_id, row.question_id, row.status,
                         row.started_at, row.finished_at, row.latency_ms, row.input_tokens,
                         row.output_tokens, row.cost, row.error)
