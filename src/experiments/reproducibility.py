"""Reproducibility contracts for evaluation experiments."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json


@dataclass(frozen=True)
class ReproducibilitySnapshot:
    schema_version: str
    model_version: str
    embedding_version: str
    retriever_version: str
    prompt_version: str
    evaluator_versions: dict[str, str]
    benchmark_version: str
    runtime_version: str

    def canonical(self) -> dict:
        return {
            "schema_version": self.schema_version,
            "model_version": self.model_version,
            "embedding_version": self.embedding_version,
            "retriever_version": self.retriever_version,
            "prompt_version": self.prompt_version,
            "evaluator_versions": dict(sorted(self.evaluator_versions.items())),
            "benchmark_version": self.benchmark_version,
            "runtime_version": self.runtime_version,
        }

    @property
    def config_hash(self) -> str:
        raw = json.dumps(self.canonical(), sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def as_dict(self) -> dict:
        payload = self.canonical()
        payload["config_hash"] = self.config_hash
        return payload
