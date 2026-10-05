import unittest

from src.experiments.statistics import compare_experiment_results, render_statistical_markdown
from src.experiments.models import ExperimentResult, RunRecord
from datetime import datetime


def result(qid, value):
    return ExperimentResult(
        run=RunRecord(
            f"run-{qid}", "exp", qid, "completed",
            datetime(2026, 1, 1), datetime(2026, 1, 1),
            1.0, None, None, None,
        ),
        answer=type(
            "Evaluation", (), {
                "metrics": type("Metrics", (), {"correctness": value})()
            }
        )(),
    )


class StatisticalComparisonTests(unittest.TestCase):
    def test_comparison_requires_paired_results(self):
        report = compare_experiment_results(
            "exp-a",
            [result("q1", 0.4), result("q2", 0.5)],
            "exp-b",
            [result("q1", 0.6), result("q2", 0.7)],
            benchmark_version="ClinicalQA-v2",
            metrics=[("answer", "correctness")],
            bootstrap_iterations=100,
        )
        self.assertEqual(report.benchmark_version, "ClinicalQA-v2")
        self.assertEqual(len(report.comparisons), 1)
        self.assertAlmostEqual(report.comparisons[0].mean_difference, 0.2)

        rendered = render_statistical_markdown(report)
        self.assertIn("answer.correctness", rendered)
        self.assertIn("Cohen dz", rendered)


if __name__ == "__main__":
    unittest.main()
