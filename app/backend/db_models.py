from datetime import date, datetime
from sqlalchemy import Date, DateTime, Float, Integer, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.backend.database import Base


class DocumentRow(Base):
    __tablename__ = "documents"
    document_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    title: Mapped[str] = mapped_column(String(500))
    source: Mapped[str] = mapped_column(String(500))
    organization: Mapped[str] = mapped_column(String(500))
    publication_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    url: Mapped[str] = mapped_column(String(2000))
    content: Mapped[str] = mapped_column(Text)


class ChunkRow(Base):
    __tablename__ = "chunks"
    chunk_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    document_id: Mapped[str] = mapped_column(String(64), index=True)
    text: Mapped[str] = mapped_column(Text)
    section: Mapped[str | None] = mapped_column(String(500), nullable=True)
    page: Mapped[int | None] = mapped_column(Integer, nullable=True)
    chunk_index: Mapped[int] = mapped_column(Integer)
    embedding: Mapped[list | None] = mapped_column(JSON, nullable=True)


class ExperimentRow(Base):
    __tablename__ = "experiments"
    experiment_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(500))
    description: Mapped[str] = mapped_column(Text)
    model_config: Mapped[dict] = mapped_column(JSON)
    embedding_config: Mapped[dict] = mapped_column(JSON)
    retriever_config: Mapped[dict] = mapped_column(JSON)
    top_k: Mapped[int] = mapped_column(Integer)
    prompt_version: Mapped[str] = mapped_column(String(100))
    benchmark_version: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(DateTime)


class RunRow(Base):
    __tablename__ = "runs"
    run_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    experiment_id: Mapped[str] = mapped_column(String(64), index=True)
    question_id: Mapped[str] = mapped_column(String(100), index=True)
    status: Mapped[str] = mapped_column(String(50))
    started_at: Mapped[datetime] = mapped_column(DateTime)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    latency_ms: Mapped[float | None] = mapped_column(Float, nullable=True)
    input_tokens: Mapped[int | None] = mapped_column(Integer, nullable=True)
    output_tokens: Mapped[int | None] = mapped_column(Integer, nullable=True)
    cost: Mapped[float | None] = mapped_column(Float, nullable=True)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)


class AnswerRow(Base):
    __tablename__ = "answers"
    answer_id: Mapped[str] = mapped_column(String(100), primary_key=True)
    run_id: Mapped[str] = mapped_column(String(64), index=True)
    answer_text: Mapped[str] = mapped_column(Text)
    claims: Mapped[list] = mapped_column(JSON)
    uncertainty: Mapped[str | None] = mapped_column(Text, nullable=True)
    model: Mapped[str] = mapped_column(String(200))
    prompt_version: Mapped[str] = mapped_column(String(100))


class CitationRow(Base):
    __tablename__ = "citations"
    citation_id: Mapped[str] = mapped_column(String(150), primary_key=True)
    answer_id: Mapped[str] = mapped_column(String(100), index=True)
    claim_index: Mapped[int] = mapped_column(Integer)
    chunk_id: Mapped[str] = mapped_column(String(64), index=True)
    citation_text: Mapped[str] = mapped_column(Text)


class EvaluationRow(Base):
    __tablename__ = "evaluations"
    evaluation_id: Mapped[str] = mapped_column(String(100), primary_key=True)
    answer_id: Mapped[str] = mapped_column(String(100), index=True)
    evaluator_version: Mapped[str] = mapped_column(String(100))
    scores: Mapped[dict] = mapped_column(JSON)
    details: Mapped[dict] = mapped_column(JSON)


class FailureRow(Base):
    __tablename__ = "failures"
    failure_id: Mapped[str] = mapped_column(String(150), primary_key=True)
    run_id: Mapped[str] = mapped_column(String(64), index=True)
    question_id: Mapped[str] = mapped_column(String(100), index=True)
    answer_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    category: Mapped[str] = mapped_column(String(100), index=True)
    type: Mapped[str] = mapped_column(String(200), index=True)
    severity: Mapped[str] = mapped_column(String(20), index=True)
    description: Mapped[str] = mapped_column(Text)
    evidence: Mapped[str] = mapped_column(Text)
    metric: Mapped[str | None] = mapped_column(String(200), nullable=True)
    metric_value: Mapped[float | None] = mapped_column(Float, nullable=True)
    classifier_version: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
