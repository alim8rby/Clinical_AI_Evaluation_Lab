import unittest

from src.evaluation.benchmark_v2 import (
    BenchmarkV2Question,
    BenchmarkV2ValidationError,
    validate_benchmark_v2_payload,
)


class BenchmarkV2Tests(unittest.TestCase):
    def _item(self):
        return {
            "question_id": "cq2-001",
            "question": "What is depression?",
            "domain": "depression",
            "difficulty": "easy",
            "question_type": "fact",
            "safety_relevance": False,
            "expected_evidence": ["chunk-1"],
            "reference_answer": "A controlled answer.",
            "key_concepts": ["depression"],
        }

    def test_valid_question(self):
        question = BenchmarkV2Question(
            question_id="cq2-001",
            question="What is depression?",
            domain="depression",
            difficulty="easy",
            question_type="fact",
            safety_relevance=False,
            expected_evidence=("chunk-1",),
            reference_answer="A controlled answer.",
            key_concepts=("depression",),
        )
        self.assertEqual(question.question_type, "fact")

    def test_rejects_invalid_question_type(self):
        item = self._item()
        item["question_type"] = "other"
        with self.assertRaises(BenchmarkV2ValidationError):
            validate_benchmark_v2_payload([item])

    def test_rejects_duplicate_ids(self):
        item = self._item()
        with self.assertRaises(BenchmarkV2ValidationError):
            validate_benchmark_v2_payload([item, dict(item)])

    def test_rejects_invalid_fields(self):
        item = self._item()
        item["unexpected"] = True
        with self.assertRaises(BenchmarkV2ValidationError):
            validate_benchmark_v2_payload([item])


if __name__ == "__main__":
    unittest.main()
