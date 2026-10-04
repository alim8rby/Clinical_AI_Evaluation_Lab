from sqlalchemy.orm import Session
from app.backend.database import SessionLocal
from app.backend.runtime import EvaluationRuntime
from src.failure_analysis import FailureObservatory
from src.pipeline import ClinicalRAG

class ApiServices:
    def __init__(self, rag: ClinicalRAG | None = None):
        self.rag=rag
        self._failure_observatory=None
    def session(self) -> Session:
        return SessionLocal()
    def runtime(self, session: Session) -> EvaluationRuntime:
        if self.rag is None: raise RuntimeError("QA service is not configured")
        return EvaluationRuntime(session,self.rag)
    @property
    def observatory(self):
        if self._failure_observatory is None:
            from app.backend.repositories import FailureRepository
            self._failure_observatory=FailureObservatory(FailureRepository(self.session()))
        return self._failure_observatory

services=ApiServices()
