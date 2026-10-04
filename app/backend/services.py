from pathlib import Path
import os

from src.failure_analysis import FailureObservatory, FailureStore
from src.pipeline import ClinicalRAG


class ApiServices:
    """Application dependencies. Infrastructure implementations arrive in later V4 phases."""

    def __init__(self, rag: ClinicalRAG | None = None, observatory: FailureObservatory | None = None):
        self.rag = rag
        store_path = Path(os.getenv("FAILURE_STORE_PATH", "data/processed/failures.json"))
        self.observatory = observatory or FailureObservatory(FailureStore(store_path))


services = ApiServices()
