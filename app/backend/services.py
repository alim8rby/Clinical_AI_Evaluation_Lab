import json
from datetime import date
from pathlib import Path

from sqlalchemy.orm import Session

from app.backend.database import DATABASE_URL, SessionLocal
from app.backend.runtime import EvaluationRuntime
from app.backend.repositories import ChunkEmbeddingRepository, ChunkRepository, DocumentRepository
from src.failure_analysis import FailureObservatory, FailureQuery
from src.generation import OllamaGenerationProvider, build_citations
from src.ingestion.models import SourceDocument
from src.pipeline import ClinicalRAG, RAGResult
from src.preprocessing import chunk_document
from src.retrieval import (
    LocalHashedEmbeddingProvider,
    PgVectorRetriever,
    VectorIndex,
    retrieve,
)


class DatabaseClinicalRAG:
    """Infrastructure adapter that keeps the V1 RAG result contract over PostgreSQL retrieval."""

    def __init__(self, session_factory, generator):
        self.session_factory = session_factory
        self.generator = generator
        self.embedder = LocalHashedEmbeddingProvider(dimensions=256)

    def ingest(self, document: SourceDocument, *, max_chars: int = 1200):
        chunks = chunk_document(document, max_chars=max_chars)
        session = self.session_factory()
        try:
            DocumentRepository(session).save(document)
            ChunkRepository(session).save_many(chunks)
            ChunkEmbeddingRepository(session).save_many(
                chunks, [self.embedder.embed(chunk.text) for chunk in chunks]
            )
        finally:
            session.close()
        return chunks

    def ask(self, question: str, *, top_k: int = 5, answer_id: str = "answer-1", prompt_version: str = "v1"):
        session = self.session_factory()
        try:
            evidence = PgVectorRetriever(session, self.embedder).retrieve(question, top_k=top_k)
            answer = self.generator.generate(question, evidence, prompt_version=prompt_version)
            citations = build_citations(answer, evidence, answer_id=answer_id)
            return RAGResult(
                question=question,
                chunks=[item.chunk for item in evidence.evidence],
                evidence=evidence,
                answer=answer,
                citations=citations,
            )
        finally:
            session.close()


class DatabaseFailureObservatory:
    """Request-scoped adapter that prevents a long-lived database session."""

    def __init__(self, session_factory):
        self.session_factory = session_factory

    def _run(self, operation):
        from app.backend.repositories import FailureRepository

        session = self.session_factory()
        try:
            return operation(FailureObservatory(FailureRepository(session)))
        finally:
            session.close()

    def get_failure(self, failure_id):
        return self._run(lambda observatory: observatory.get_failure(failure_id))

    def list_failures(self, query: FailureQuery):
        return self._run(lambda observatory: observatory.list_failures(query))

    def summary(self, query: FailureQuery):
        return self._run(lambda observatory: observatory.summary(query))

    def snapshot(self, query: FailureQuery):
        return self._run(lambda observatory: observatory.snapshot(query))


class ApiServices:
    def readiness(self):
        return {"rag": self.rag is not None, "database": self._database_ready()}

    def _database_ready(self):
        try:
            from sqlalchemy import text

            session = self.session()
            try:
                session.execute(text("SELECT 1"))
                return True
            finally:
                session.close()
        except Exception:
            return False

    def __init__(self, rag=None):
        self.rag = rag
        self._failure_observatory = None

    def session(self) -> Session:
        return SessionLocal()

    def runtime(self, session: Session) -> EvaluationRuntime:
        if self.rag is None:
            raise RuntimeError("QA service is not configured")
        return EvaluationRuntime(session, self.rag)

    @property
    def observatory(self):
        if self._failure_observatory is None:
            self._failure_observatory = DatabaseFailureObservatory(self.session)
        return self._failure_observatory

    @observatory.setter
    def observatory(self, value):
        self._failure_observatory = value


def _load_controlled_documents():
    root = Path(__file__).resolve().parents[2]
    source_path = root / "data" / "raw" / "controlled" / "depression_sources.json"
    if not source_path.exists():
        return []
    payload = json.loads(source_path.read_text(encoding="utf-8"))
    return [
        SourceDocument(
            document_id=item["document_id"],
            title=item["title"],
            source=item["source"],
            organization=item["organization"],
            publication_date=date.fromisoformat(item["publication_date"])
            if item.get("publication_date")
            else None,
            url=item["url"],
            content=item["content"],
        )
        for item in payload
    ]


def build_default_rag():
    documents = _load_controlled_documents()
    if not documents:
        return None

    generator = OllamaGenerationProvider()
    if DATABASE_URL.startswith(("postgresql://", "postgresql+psycopg://")):
        rag = DatabaseClinicalRAG(SessionLocal, generator)
    else:
        rag = ClinicalRAG(VectorIndex("data/caiel-dev-index.json"), generator)

    for document in documents:
        rag.ingest(document)
    return rag


services = ApiServices(build_default_rag())
