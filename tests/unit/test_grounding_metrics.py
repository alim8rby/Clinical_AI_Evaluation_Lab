import unittest

from src.evaluation.grounding_metrics import evaluate_grounding
from src.generation.citations import Citation
from src.generation.models import Answer, Claim
from src.preprocessing.models import Chunk
from src.retrieval.search import Evidence, EvidenceSet


class GroundingMetricTests(unittest.TestCase):
    def _evidence(self):
        chunk = Chunk("chunk-1", "doc-1", "Depression involves persistent low mood and loss of interest.", None, None, 0)
        return EvidenceSet("question", [Evidence(chunk, 1.0, 1)])

    def test_supported_claim(self):
        answer = Answer(
            "Depression involves persistent low mood.",
            [Claim("Depression involves persistent low mood.", [1])],
            None, "mock-v1", "v1",
        )
        citation = Citation("c1", "answer-1", 1, "chunk-1", "chunk-1")
        result = evaluate_grounding(answer, [citation], self._evidence())
        self.assertEqual(result.citation_coverage, 1.0)
        self.assertEqual(result.citation_validity, 1.0)
        self.assertGreater(result.faithfulness, 0.5)
        self.assertLess(result.unsupported_claim_rate, 0.5)

    def test_uncited_claim_is_unsupported(self):
        answer = Answer(
            "Depression involves persistent low mood.",
            [Claim("Depression involves persistent low mood.", [])],
            None, "mock-v1", "v1",
        )
        result = evaluate_grounding(answer, [], self._evidence())
        self.assertEqual(result.citation_coverage, 0.0)
        self.assertEqual(result.citation_validity, 0.0)
        self.assertEqual(result.unsupported_claim_rate, 1.0)

    def test_invalid_citation(self):
        answer = Answer(
            "Depression involves persistent low mood.",
            [Claim("Depression involves persistent low mood.", [1])],
            None, "mock-v1", "v1",
        )
        citation = Citation("c1", "answer-1", 1, "missing", "missing")
        result = evaluate_grounding(answer, [citation], self._evidence())
        self.assertEqual(result.citation_coverage, 1.0)
        self.assertEqual(result.citation_validity, 0.0)
