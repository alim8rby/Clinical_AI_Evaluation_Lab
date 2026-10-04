import json
import unittest
from pathlib import Path

from src.evaluation.retrieval_challenge import (
    assert_challenge_evidence_resolved,
    validate_challenge_payload,
)
from src.ingestion.models import SourceDocument
from src.preprocessing.chunk import chunk_document


ROOT = Path(__file__).parents[2]


class RetrievalChallengeTests(unittest.TestCase):
    def test_challenge_set_resolves_and_has_required_mix(self):
        payload = json.loads(
            (ROOT / "data/benchmark/clinicalqa_v1_challenge.json").read_text(encoding="utf-8")
        )
        sources = json.loads(
            (ROOT / "data/raw/controlled/depression_sources.json").read_text(encoding="utf-8")
        )
        chunk_ids = set()
        for source in sources:
            chunk_ids.update(
                chunk.chunk_id
                for chunk in chunk_document(SourceDocument(**source))
            )

        cases = validate_challenge_payload(payload)
        assert_challenge_evidence_resolved(cases, chunk_ids)

        self.assertEqual(len(cases), 12)
        self.assertEqual(
            {case.challenge_type for case in cases},
            {"lexical_mismatch", "multi_evidence", "ranking"},
        )
        self.assertEqual(
            {case.difficulty for case in cases},
            {"easy", "medium", "hard"},
        )

    def test_expected_and_distractors_are_disjoint(self):
        payload = json.loads(
            (ROOT / "data/benchmark/clinicalqa_v1_challenge.json").read_text(encoding="utf-8")
        )
        cases = validate_challenge_payload(payload)
        for case in cases:
            self.assertTrue(set(case.expected_evidence).isdisjoint(case.distractor_evidence))


if __name__ == "__main__":
    unittest.main()
