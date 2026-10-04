import json
import unittest
from collections import Counter
from pathlib import Path

from src.evaluation.benchmark_v2 import assert_evidence_resolved, validate_benchmark_v2_payload
from src.ingestion.models import SourceDocument
from src.preprocessing.chunk import chunk_document

ROOT = Path(__file__).parents[2]


class BenchmarkV2IntegrationTests(unittest.TestCase):
    def test_clinicalqa_v2_is_complete_and_resolves(self):
        sources = json.loads(
            (ROOT / "data/raw/controlled/depression_sources.json").read_text(encoding="utf-8")
        )
        payload = json.loads(
            (ROOT / "data/benchmark/clinicalqa_v2.json").read_text(encoding="utf-8")
        )

        chunk_ids = set()
        for source in sources:
            document = SourceDocument(**source)
            chunk_ids.update(chunk.chunk_id for chunk in chunk_document(document))

        questions = validate_benchmark_v2_payload(payload)
        assert_evidence_resolved(questions, chunk_ids)

        self.assertEqual(len(questions), 60)
        self.assertEqual(len({q.question_id for q in questions}), 60)
        self.assertEqual({q.difficulty for q in questions}, {"easy", "medium", "hard"})
        self.assertEqual(
            {q.question_type for q in questions},
            {"fact", "comparison", "reasoning", "scenario", "safety"},
        )
        self.assertTrue(all(q.question_id.startswith(("cq-", "cq2-")) for q in questions))

        types = Counter(q.question_type for q in questions)
        self.assertGreaterEqual(types["fact"], 10)
        self.assertGreaterEqual(types["comparison"], 5)
        self.assertGreaterEqual(types["reasoning"], 15)
        self.assertGreaterEqual(types["scenario"], 5)
        self.assertGreaterEqual(types["safety"], 3)

        safety = sum(q.safety_relevance for q in questions)
        self.assertGreaterEqual(safety, 10)

        multi_evidence = sum(len(q.expected_evidence) > 1 for q in questions)
        self.assertGreaterEqual(multi_evidence, 8)


if __name__ == "__main__":
    unittest.main()
