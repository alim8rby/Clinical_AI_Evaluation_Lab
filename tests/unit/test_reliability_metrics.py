import unittest

from src.evaluation.grounding_metrics import GroundingMetrics
from src.evaluation.reliability_metrics import evaluate_reliability
from src.generation.models import Answer, Claim


class ReliabilityMetricTests(unittest.TestCase):
    def _grounding(self, unsupported=0.0):
        return GroundingMetrics(1.0, 1.0, 1.0 - unsupported, unsupported)

    def test_grounded_answer_has_low_hallucination_rate(self):
        answer = Answer("Supported answer.", [Claim("Supported answer.", [1])], None, "mock-v1", "v1")
        result = evaluate_reliability(answer, self._grounding())
        self.assertEqual(result.hallucination_rate, 0.0)
        self.assertEqual(result.critical_error_rate, 0.0)

    def test_unsupported_safety_answer_flags_critical_signal(self):
        answer = Answer(
            "The patient has suicidal risk.",
            [Claim("The patient has suicidal risk.", [])],
            None, "mock-v1", "v1",
        )
        result = evaluate_reliability(answer, self._grounding(1.0))
        self.assertEqual(result.hallucination_rate, 1.0)
        self.assertEqual(result.critical_error_rate, 1.0)

    def test_uncertainty_is_recorded(self):
        answer = Answer("Insufficient evidence.", [Claim("Insufficient evidence.", [])], "Evidence is insufficient.", "mock-v1", "v1")
        result = evaluate_reliability(answer, self._grounding(1.0))
        self.assertEqual(result.uncertainty_handling, 1.0)

    def test_uncited_recommendation_is_flagged(self):
        answer = Answer(
            "The patient should start treatment.",
            [Claim("The patient should start treatment.", [])],
            None, "mock-v1", "v1",
        )
        result = evaluate_reliability(answer, self._grounding(1.0))
        self.assertEqual(result.unsupported_recommendation_rate, 1.0)
