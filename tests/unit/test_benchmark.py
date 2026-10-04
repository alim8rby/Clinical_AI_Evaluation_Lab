import unittest

from src.evaluation.benchmark import BenchmarkValidationError, validate_benchmark_payload

VALID = [{
    "question_id": "cq-001",
    "question": "What is depression?",
    "domain": "depression",
    "difficulty": "easy",
    "expected_evidence": ["chunk-001"],
    "reference_answer": "A depressive disorder is characterized by persistent low mood or loss of interest with associated symptoms and impairment.",
    "key_concepts": ["depressed mood", "loss of interest", "functional impairment"],
}]

class BenchmarkTests(unittest.TestCase):
    def test_valid_payload(self):
        result = validate_benchmark_payload(VALID)
        self.assertEqual(result[0].question_id, "cq-001")

    def test_rejects_wrong_domain(self):
        with self.assertRaises(BenchmarkValidationError):
            validate_benchmark_payload([dict(VALID[0], domain="anxiety")])

    def test_rejects_duplicate_ids(self):
        with self.assertRaises(BenchmarkValidationError):
            validate_benchmark_payload(VALID + VALID)

    def test_rejects_missing_field(self):
        payload = [dict(VALID[0])]
        del payload[0]["key_concepts"]
        with self.assertRaises(BenchmarkValidationError):
            validate_benchmark_payload(payload)

    def test_rejects_empty_evidence(self):
        with self.assertRaises(BenchmarkValidationError):
            validate_benchmark_payload([dict(VALID[0], expected_evidence=[])])
