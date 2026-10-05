import unittest
from datetime import datetime

from src.experiments.engine import batch_configuration, run_batch
from src.experiments.models import Experiment, ExperimentConfig, ExperimentResult, RunRecord


def make_experiment():
    config = ExperimentConfig(
        model_config={"model": "mock-v1"},
        embedding_config={"provider": "local"},
        retriever_config={"strategy": "dense", "top_k": 5},
        top_k=5,
        prompt_version="v1",
        benchmark_version="ClinicalQA-v2",
    )
    return Experiment.create(
        "batch-test",
        "test experiment",
        config,
        created_at=datetime(2026, 1, 1),
    )


def result_for(experiment, question_id):
    run = RunRecord(
        f"run-{question_id}", experiment.experiment_id, question_id,
        "completed", datetime(2026, 1, 1), datetime(2026, 1, 1),
        1.0, 1, 1, 0.0, None,
    )
    return ExperimentResult(run=run)


class Question:
    def __init__(self, question_id):
        self.question_id = question_id


class RuntimeResult:
    def __init__(self, result):
        self.result = result


class ExperimentEngineTests(unittest.TestCase):
    def test_batch_completes_and_retains_errors(self):
        experiment = make_experiment()

        def runner(exp, question):
            if question.question_id == "q2":
                raise RuntimeError("provider unavailable")
            return RuntimeResult(result_for(exp, question.question_id))

        batch = run_batch(
            experiment,
            [Question("q1"), Question("q2"), Question("q3")],
            runner,
        )
        self.assertEqual(batch.total_questions, 3)
        self.assertEqual(batch.completed_questions, 2)
        self.assertEqual(batch.failed_questions, 1)
        self.assertEqual(len(batch.results), 2)
        self.assertEqual(batch.errors[0]["question_id"], "q2")
        self.assertAlmostEqual(batch.success_rate, 2 / 3)

    def test_stop_on_error_is_explicit(self):
        experiment = make_experiment()

        def runner(exp, question):
            if question.question_id == "q1":
                raise ValueError("bad input")
            return result_for(exp, question.question_id)

        batch = run_batch(
            experiment,
            [Question("q1"), Question("q2")],
            runner,
            stop_on_error=True,
        )
        self.assertEqual(batch.completed_questions, 0)
        self.assertEqual(batch.failed_questions, 1)

    def test_configuration_snapshot_is_stable(self):
        experiment = make_experiment()
        snapshot = batch_configuration(experiment)
        self.assertEqual(snapshot["experiment_id"], experiment.experiment_id)
        self.assertEqual(snapshot["benchmark_version"], "ClinicalQA-v2")
        self.assertEqual(snapshot["top_k"], 5)


if __name__ == "__main__":
    unittest.main()
