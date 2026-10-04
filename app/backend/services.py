import json
from datetime import date
from pathlib import Path

from sqlalchemy.orm import Session

from app.backend.database import SessionLocal
from app.backend.runtime import EvaluationRuntime
from src.failure_analysis import FailureObservatory
from src.generation import OllamaGenerationProvider
from src.ingestion.models import SourceDocument
from src.pipeline import ClinicalRAG
from src.retrieval import VectorIndex

class ApiServices:
    def __init__(self, rag=None):
        self.rag=rag
        self._failure_observatory=None

    def session(self) -> Session:
        return SessionLocal()

    def runtime(self, session: Session) -> EvaluationRuntime:
        if self.rag is None:
            raise RuntimeError("QA service is not configured")
        return EvaluationRuntime(session,self.rag)

    @property
    def observatory(self):
        if self._failure_observatory is None:
            from app.backend.repositories import FailureRepository
            session=self.session()
            self._failure_observatory=FailureObservatory(FailureRepository(session))
        return self._failure_observatory

def build_default_rag():
    root=Path(__file__).resolve().parents[2]
    source_path=root/"data"/"raw"/"controlled"/"depression_sources.json"
    if not source_path.exists():
        return None
    index=VectorIndex()
    generator=OllamaGenerationProvider()
    rag=ClinicalRAG(index,generator)
    payload=json.loads(source_path.read_text(encoding="utf-8"))
    for item in payload:
        document=SourceDocument(
            document_id=item["document_id"], title=item["title"], source=item["source"],
            organization=item["organization"], publication_date=date.fromisoformat(item["publication_date"]) if item.get("publication_date") else None,
            url=item["url"], content=item["content"],
        )
        rag.ingest(document)
    return rag

services=ApiServices(build_default_rag())
