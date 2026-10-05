import unittest
from datetime import datetime

from src.experiments.models import Experiment, ExperimentConfig
from src.experiments.reproducibility import ReproducibilitySnapshot


class ReproducibilityTests(unittest.TestCase):
    def test_snapshot_hash_is_deterministic(self):
        first = ReproducibilitySnapshot(
            "v5.9", "llama3.2:3b", "nomic-embed-text", "dense-v1",
            "prompt-v1", {"answer": "answer-v1", "retrieval": "retrieval-v1"},
            "ClinicalQA-v2", "caiel-runtime-v1",
        )
        second = ReproducibilitySnapshot(
            "v5.9", "llama3.2:3b", "nomic-embed-text", "dense-v1",
            "prompt-v1", {"retrieval": "retrieval-v1", "answer": "answer-v1"},
            "ClinicalQA-v2", "caiel-runtime-v1",
        )
        self.assertEqual(first.config_hash, second.config_hash)

    def test_experiment_identity_changes_with_version(self):
        base = ExperimentConfig({}, {}, {}, 5, "prompt-v1", "ClinicalQA-v2", model_version="model-a")
        changed = ExperimentConfig({}, {}, {}, 5, "prompt-v1", "ClinicalQA-v2", model_version="model-b")
        created = datetime(2026, 1, 1)
        self.assertNotEqual(
            Experiment.create("same", "same", base, created_at=created).experiment_id,
            Experiment.create("same", "same", changed, created_at=created).experiment_id,
        )

    def test_snapshot_contains_all_reproducibility_dimensions(self):
        config = ExperimentConfig(
            {"model": "model-a"},
            {"model": "embed-a"},
            {"version": "retriever-a"},
            5,
            "prompt-v1",
            "ClinicalQA-v2",
            model_version="model-a",
            embedding_version="embed-a",
            retriever_version="retriever-a",
            evaluator_versions={"answer": "answer-v1"},
            runtime_version="runtime-a",
        )
        snapshot = config.reproducibility_snapshot().as_dict()
        self.assertEqual(snapshot["model_version"], "model-a")
        self.assertEqual(snapshot["embedding_version"], "embed-a")
        self.assertEqual(snapshot["retriever_version"], "retriever-a")
        self.assertEqual(snapshot["evaluator_versions"]["answer"], "answer-v1")
        self.assertEqual(snapshot["benchmark_version"], "ClinicalQA-v2")
        self.assertIn("config_hash", snapshot)


if __name__ == "__main__":
    unittest.main()
