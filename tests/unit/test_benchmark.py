import unittest

from src.evaluation.benchmark import (
    BenchmarkValidationError,
    assert_evidence_resolved,
    unresolved_evidence,
    validate_benchmark_payload,
)

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

    def test_evidence_resolves(self):
        questions = validate_benchmark_payload(VALID)
        self.assertEqual(unresolved_evidence(questions, {"chunk-001"}), {})
        assert_evidence_resolved(questions, {"chunk-001"})

    def test_evidence_gate_rejects_missing_chunk(self):
        questions = validate_benchmark_payload(VALID)
        with self.assertRaises(BenchmarkValidationError):
            assert_evidence_resolved(questions, set())

    def test_deferred_marker_is_unresolved(self):
        payload = [dict(VALID[0], expected_evidence=["DEFERRED_TO_CONTROLLED_CORPUS"])]
        questions = validate_benchmark_payload(payload)
        self.assertIn("cq-001", unresolved_evidence(questions, {"chunk-001"}))

    def test_clinicalqa_v1_chunk_ids_are_stable(self):
        expected = {
            "cq-001": "chunk_8cdc380723ba4f0c",
            "cq-002": "chunk_75092e03f18cfb22",
            "cq-003": "chunk_0b161e000d97f624",
            "cq-004": "chunk_4492f3fed67d11ff",
            "cq-005": "chunk_9a1d40e76f9ce39f",
            "cq-006": "chunk_fc1b23978839cab5",
            "cq-007": "chunk_76d79d3e08d6782d",
            "cq-008": "chunk_2463f3d3f087914f",
        }
        for question_id, chunk_id in expected.items():
            self.assertTrue(chunk_id.startswith("chunk_"))
