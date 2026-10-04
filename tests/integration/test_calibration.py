import json
from pathlib import Path
import unittest

from src.evaluation.calibration import evaluate_calibration, validate_calibration_payload


class CalibrationDatasetIntegrationTests(unittest.TestCase):
    def test_controlled_calibration_dataset_is_versioned_and_valid(self):
        path = Path("data/calibration/clinicalqa_v1_calibration.json")
        payload = json.loads(path.read_text(encoding="utf-8"))
        labels = validate_calibration_payload(payload)
        self.assertEqual(labels, [])
        self.assertEqual(evaluate_calibration(labels), [])


if __name__ == "__main__":
    unittest.main()
