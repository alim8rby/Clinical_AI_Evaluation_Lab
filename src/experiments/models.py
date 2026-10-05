"""Experiment and run models for reproducible evaluation."""
from dataclasses import dataclass
from datetime import datetime
import hashlib
import json

@dataclass(frozen=True)
class ExperimentConfig:
    model_config: dict
    embedding_config: dict
    retriever_config: dict
    top_k: int
    prompt_version: str
    benchmark_version: str
    model_version: str = "unspecified"
    embedding_version: str = "unspecified"
    retriever_version: str = "unspecified"
    evaluator_versions: dict[str, str] | None = None
    runtime_version: str = "caiel-runtime-v1"
    def __post_init__(self):
        if self.top_k <= 0: raise ValueError("top_k must be greater than zero")
        if not self.prompt_version.strip(): raise ValueError("prompt_version must not be empty")
        if not self.benchmark_version.strip(): raise ValueError("benchmark_version must not be empty")
        for name, value in (("model_version", self.model_version), ("embedding_version", self.embedding_version), ("retriever_version", self.retriever_version), ("runtime_version", self.runtime_version)):
            if not str(value).strip(): raise ValueError(f"{name} must not be empty")
        if self.evaluator_versions is not None:
            for key, value in self.evaluator_versions.items():
                if not str(key).strip() or not str(value).strip(): raise ValueError("evaluator_versions must contain non-empty names and versions")

    def reproducibility_snapshot(self):
        from src.experiments.reproducibility import ReproducibilitySnapshot
        return ReproducibilitySnapshot(
            schema_version="v5.9",
            model_version=self.model_version,
            embedding_version=self.embedding_version,
            retriever_version=self.retriever_version,
            prompt_version=self.prompt_version,
            evaluator_versions=dict(self.evaluator_versions or {}),
            benchmark_version=self.benchmark_version,
            runtime_version=self.runtime_version,
        )

@dataclass(frozen=True)
class Experiment:
    experiment_id: str
    name: str
    description: str
    config: ExperimentConfig
    created_at: datetime
    @staticmethod
    def create(name, description, config, *, created_at):
        if not name.strip(): raise ValueError("name must not be empty")
        raw=json.dumps({"name":name,"description":description,"model_config":config.model_config,"embedding_config":config.embedding_config,"retriever_config":config.retriever_config,"top_k":config.top_k,"prompt_version":config.prompt_version,"benchmark_version":config.benchmark_version},sort_keys=True)
        return Experiment("exp_"+hashlib.sha256(raw.encode()).hexdigest()[:16],name,description,config,created_at)

@dataclass(frozen=True)
class RunRecord:
    run_id: str
    experiment_id: str
    question_id: str
    status: str
    started_at: datetime
    finished_at: datetime | None
    latency_ms: float | None
    input_tokens: int | None
    output_tokens: int | None
    cost: float | None
    error: str | None = None

@dataclass(frozen=True)
class ExperimentResult:
    run: RunRecord
    retrieval: object | None = None
    answer: object | None = None
    grounding: object | None = None
    reliability: object | None = None
    failures: tuple[dict, ...] = ()
