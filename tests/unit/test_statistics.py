import unittest

from src.evaluation.statistics import extract_metric_by_question, paired_compare


class Result:
    def __init__(self, question_id, value):
        self.run = type("Run", (), {"question_id": question_id})()
        self.answer = type(
            "Evaluation", (), {"metrics": type("Metrics", (), {"correctness": value})()}
        )()


class StatisticalEvaluationTests(unittest.TestCase):
    def test_paired_compare_is_deterministic(self):
        baseline = {"q1": 0.4, "q2": 0.5, "q3": 0.6, "q4": 0.7}
        candidate = {"q1": 0.5, "q2": 0.6, "q3": 0.7, "q4": 0.8}
        first = paired_compare(
            "answer.correctness", baseline, candidate, bootstrap_iterations=500
        )
        second = paired_compare(
            "answer.correctness", baseline, candidate, bootstrap_iterations=500
        )
        self.assertEqual(first, second)
        self.assertEqual(first.n, 4)
        self.assertAlmostEqual(first.mean_difference, 0.1)
        self.assertGreaterEqual(first.ci_high, first.ci_low)

    def test_requires_paired_question_ids(self):
        with self.assertRaises(ValueError):
            paired_compare("metric", {"q1": 1.0}, {"q2": 1.0})

    def test_extracts_question_level_metric(self):
        results = [Result("q1", 0.4), Result("q2", 0.8)]
        values = extract_metric_by_question(
            results, metric_group="answer", metric_name="correctness"
        )
        self.assertEqual(values, {"q1": 0.4, "q2": 0.8})

    def test_effect_size_is_zero_for_constant_differences(self):
        result = paired_compare(
            "metric",
            {"q1": 0.2, "q2": 0.3, "q3": 0.4},
            {"q1": 0.3, "q2": 0.4, "q3": 0.5},
            bootstrap_iterations=100,
        )
        self.assertEqual(result.effect_size_dz, 0.0)


if __name__ == "__main__":
    unittest.main()
