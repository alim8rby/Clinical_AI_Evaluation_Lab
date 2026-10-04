import unittest

from src.evaluation.answer_metrics import (
    correctness_score,
    evaluate_answer,
    completeness_score,
    relevance_score,
)


class AnswerMetricTests(unittest.TestCase):
    def test_perfect_answer(self):
        reference = "Depression can involve persistent low mood and loss of interest."
        answer = "Depression can involve persistent low mood and loss of interest."
        concepts = ("persistent low mood", "loss of interest")
        result = evaluate_answer(reference, answer, concepts)
        self.assertEqual(result.correctness, 1.0)
        self.assertEqual(result.completeness, 1.0)
        self.assertEqual(result.relevance, 1.0)

    def test_partial_completeness(self):
        self.assertAlmostEqual(
            completeness_score("persistent low mood only", ("persistent low mood", "loss of interest")),
            0.5,
        )

    def test_relevance_penalizes_unrelated_terms(self):
        score = relevance_score("persistent low mood", "persistent low mood unrelated material")
        self.assertLess(score, 1.0)

    def test_correctness_is_reference_overlap(self):
        score = correctness_score("low mood and loss of interest", "low mood")
        self.assertGreater(score, 0.0)
        self.assertLess(score, 1.0)

    def test_rejects_empty_inputs(self):
        with self.assertRaises(ValueError):
            evaluate_answer("", "answer", ("concept",))
        with self.assertRaises(ValueError):
            evaluate_answer("reference", "", ("concept",))
        with self.assertRaises(ValueError):
            evaluate_answer("reference", "answer", ())
