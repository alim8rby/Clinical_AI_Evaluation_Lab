import unittest
from datetime import datetime, timezone

from src.experiments.models import Experiment, ExperimentConfig, RunRecord


class ExperimentTests(unittest.TestCase):
    def _config(self):
        return ExperimentConfig(
            model_config={"provider": "mock", "model": "mock-v1"},
            embedding_config={"provider": "local", "model": "hashed-v1"},
            retriever_config={"type": "vector", "metric": "cosine"},
            top_k=5,
            prompt_version="v1",
            benchmark_version="clinicalqa_v1",
        )

    def test_experiment_id_is_deterministic(self):
        config = self._config()
        a = Experiment.create("baseline", "Baseline run", config, created_at=datetime.now(timezone.utc))
        b = Experiment.create("baseline", "Baseline run", config, created_at=datetime.now(timezone.utc))
        self.assertEqual(a.experiment_id, b.experiment_id)

    def test_invalid_top_k_rejected(self):
        with self.assertRaises(ValueError):
            ExperimentConfig({}, {}, {}, 0, "v1", "clinicalqa_v1")

    def test_run_record_captures_reproducibility_fields(self):
        run = RunRecord(
            "run-1", "exp-1", "cq-001", "completed",
            datetime.now(timezone.utc), None, 12.5, 10, 20, 0.0, None,
        )
        self.assertEqual(run.experiment_id, "exp-1")
        self.assertEqual(run.question_id, "cq-001")
        self.assertEqual(run.status, "completed")
