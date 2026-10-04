import json
import unittest
from pathlib import Path

from src.ingestion.models import SourceDocument
from src.preprocessing.chunk import chunk_document
from src.evaluation.benchmark import assert_evidence_resolved, validate_benchmark_payload


ROOT = Path(__file__).parents[2]


class BenchmarkCorpusIntegrationTests(unittest.TestCase):
    def test_clinicalqa_v1_evidence_resolves_against_controlled_corpus(self):
        sources = json.loads(
            (ROOT / "data/raw/controlled/depression_sources.json").read_text(
                encoding="utf-8"
            )
        )
        benchmark_payload = json.loads(
            (ROOT / "data/benchmark/clinicalqa_v1.json").read_text(encoding="utf-8")
        )

        chunk_ids = set()
        for source in sources:
            document = SourceDocument(**source)
            chunk_ids.update(chunk.chunk_id for chunk in chunk_document(document))

        questions = validate_benchmark_payload(benchmark_payload)
        assert_evidence_resolved(questions, chunk_ids)

        self.assertEqual(len(questions), 40)
        self.assertEqual(len({q.question_id for q in questions}), 40)
        self.assertEqual({q.difficulty for q in questions}, {"easy", "medium", "hard"})
        self.assertEqual(len(chunk_ids), 10)
