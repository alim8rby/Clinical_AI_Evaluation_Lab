import unittest
from datetime import datetime, timezone

from src.evaluation.answer import AnswerEvaluation
from src.evaluation.answer_metrics import AnswerMetrics
from src.evaluation.report import build_report, render_markdown
from src.experiments.models import Experiment, ExperimentConfig, ExperimentResult, RunRecord


class EvaluationReportTests(unittest.TestCase):
    def test_builds_reproducible_report(self):
        config = ExperimentConfig(
            {"provider": "mock", "model": "mock-v1"},
            {"provider": "local", "model": "hashed-v1"},
            {"type": "vector"}, 5, "v1", "clinicalqa_v1",
        )
        experiment = Experiment.create(
            "baseline", "Baseline", config,
            created_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        )
        run = RunRecord(
            "run-1", experiment.experiment_id, "cq-001", "completed",
            datetime(2026, 1, 1, tzinfo=timezone.utc),
            None, None, None, None, None,
        )
        result = ExperimentResult(
            run=run,
            answer=AnswerEvaluation("cq-001", AnswerMetrics(0.8, 0.6, 0.9)),
        )
        report = build_report(experiment, [result], failures=[{"type": "hallucination"}])
        markdown = render_markdown(report)
        self.assertEqual(report.sample_count, 1)
        self.assertAlmostEqual(report.metrics["answer.correctness"], 0.8)
        self.assertIn("hallucination", markdown)
        self.assertIn("clinicalqa_v1", markdown)
