import unittest
from datetime import datetime

from src.experiments.engine import run_batch
from src.experiments.models import Experiment, ExperimentConfig, ExperimentResult, RunRecord
from src.experiments.report import build_batch_report, render_batch_markdown


def experiment():
    return Experiment.create(
        "report-test",
        "report",
        ExperimentConfig(
            {"model": "mock-v1"}, {"provider": "local"}, {"strategy": "dense"},
            5, "v1", "ClinicalQA-v2",
        ),
        created_at=datetime(2026, 1, 1),
    )


def result_for(exp, qid):
    return ExperimentResult(
        RunRecord(
            f"run-{qid}", exp.experiment_id, qid, "completed",
            datetime(2026, 1, 1), datetime(2026, 1, 1),
            2.0, 1, 2, 0.0,
        )
    )


class Q:
    def __init__(self, question_id):
        self.question_id = question_id


class BatchReportTests(unittest.TestCase):
    def test_batch_report_preserves_errors_and_configuration(self):
        exp = experiment()

        def runner(e, q):
            if q.question_id == "q2":
                raise RuntimeError("timeout")
            return result_for(e, q.question_id)

        batch = run_batch(exp, [Q("q1"), Q("q2")], runner)
        report = build_batch_report(exp, batch, failures=[{"type": "timeout"}])
        rendered = render_batch_markdown(report)

        self.assertEqual(report.evaluation.sample_count, 1)
        self.assertEqual(report.configuration["experiment_id"], exp.experiment_id)
        self.assertIn("Failed questions: 1", rendered)
        self.assertIn("timeout", rendered)


if __name__ == "__main__":
    unittest.main()
