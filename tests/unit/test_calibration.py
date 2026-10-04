import unittest

from src.evaluation.calibration import (
    CalibrationLabel,
    CalibrationValidationError,
    evaluate_calibration,
    validate_calibration_payload,
)


class CalibrationTests(unittest.TestCase):
    def test_validates_and_scores_calibration_labels(self):
        payload = [
            {"item_id": "cq-001", "dimension": "correctness", "human_score": 0.8, "model_score": 0.7},
            {"item_id": "cq-002", "dimension": "correctness", "human_score": 0.6, "model_score": 0.7},
            {"item_id": "cq-001", "dimension": "relevance", "human_score": 1.0, "model_score": 0.9},
        ]
        labels = validate_calibration_payload(payload)
        results = evaluate_calibration(labels)
        correctness = next(item for item in results if item.dimension == "correctness")
        self.assertEqual(correctness.sample_count, 2)
        self.assertAlmostEqual(correctness.mean_absolute_error, 0.1)
        self.assertAlmostEqual(correctness.mean_bias, 0.0)
        self.assertEqual(correctness.within_tolerance_rate, 1.0)

    def test_rejects_duplicate_dimension_labels(self):
        payload = [
            {"item_id": "cq-001", "dimension": "correctness", "human_score": 0.8, "model_score": 0.7},
            {"item_id": "cq-001", "dimension": "correctness", "human_score": 0.9, "model_score": 0.7},
        ]
        with self.assertRaises(CalibrationValidationError):
            validate_calibration_payload(payload)

    def test_rejects_invalid_dimension_and_score(self):
        with self.assertRaises(CalibrationValidationError):
            CalibrationLabel("cq-001", "bad", 0.5, 0.5)
        with self.assertRaises(CalibrationValidationError):
            CalibrationLabel("cq-001", "correctness", 1.1, 0.5)

    def test_empty_calibration_is_valid_but_produces_no_results(self):
        self.assertEqual(evaluate_calibration([]), [])


if __name__ == "__main__":
    unittest.main()
