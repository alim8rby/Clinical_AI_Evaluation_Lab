import json
import unittest
from pathlib import Path

from src.evaluation.calibration import validate_calibration_payload


ROOT = Path(__file__).parents[2]


class CalibrationDatasetTests(unittest.TestCase):
    def test_calibration_dataset_is_valid(self):
        payload = json.loads(
            (ROOT / "data/calibration/clinicalqa_v1_calibration.json").read_text(
                encoding="utf-8"
            )
        )
        labels = validate_calibration_payload(payload)
        self.assertEqual(labels, [])


if __name__ == "__main__":
    unittest.main()
