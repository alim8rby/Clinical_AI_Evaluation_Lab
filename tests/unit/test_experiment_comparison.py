import unittest
from datetime import datetime, timezone

from src.evaluation.answer_metrics import AnswerMetrics
from src.evaluation.answer import AnswerEvaluation
from src.experiments.comparison import compare_experiments
from src.experiments.models import Experiment, ExperimentConfig, ExperimentResult, RunRecord


class ExperimentComparisonTests(unittest.TestCase):
    def _experiment(self, name, model):
        config = ExperimentConfig(
            {"provider": "mock", "model": model},
            {"provider": "local", "model": "hashed-v1"},
            {"type": "vector"},
            5, "v1", "clinicalqa_v1",
        )
        return Experiment.create(name, "test", config, created_at=datetime.now(timezone.utc))

    def _result(self, experiment_id, question_id, correctness):
        run = RunRecord(
            f"run-{question_id}", experiment_id, question_id, "completed",
            datetime.now(timezone.utc), None, None, None, None, None, None,
        )
        answer = AnswerEvaluation(question_id, AnswerMetrics(correctness, correctness, correctness))
        return ExperimentResult(run=run, answer=answer)

    def test_compares_shared_metrics(self):
        baseline = self._experiment("baseline", "model-a")
        candidate = self._experiment("candidate", "model-b")
        comparison = compare_experiments(
            baseline, candidate,
            [self._result(baseline.experiment_id, "q1", 0.5)],
            [self._result(candidate.experiment_id, "q1", 0.8)],
        )
        self.assertEqual(comparison.benchmark_version, "clinicalqa_v1")
        self.assertEqual(comparison.baseline_samples, 1)
        self.assertEqual(comparison.candidate_samples, 1)
        self.assertAlmostEqual(comparison.metric_deltas[0].delta, 0.3)

    def test_rejects_different_benchmarks(self):
        baseline = self._experiment("baseline", "model-a")
        candidate = Experiment.create(
            "candidate", "test",
            ExperimentConfig({}, {}, {}, 5, "v1", "clinicalqa_v2"),
            created_at=datetime.now(timezone.utc),
        )
        with self.assertRaises(ValueError):
            compare_experiments(baseline, candidate, [], [])

    def test_rejects_same_experiment(self):
        experiment = self._experiment("same", "model-a")
        with self.assertRaises(ValueError):
            compare_experiments(experiment, experiment, [], [])
