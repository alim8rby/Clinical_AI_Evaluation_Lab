import unittest

from src.evaluation.benchmark import BenchmarkQuestion
from src.evaluation.retrieval import evaluate_question_retrieval
from src.preprocessing.models import Chunk
from src.retrieval.search import Evidence, EvidenceSet


class RetrievalEvaluationTests(unittest.TestCase):
    def test_evaluates_evidence_set_against_question(self):
        question = BenchmarkQuestion(
            question_id="cq-001",
            question="What is depression?",
            domain="depression",
            difficulty="easy",
            expected_evidence=("chunk-b",),
            reference_answer="reference",
            key_concepts=("mood",),
        )
        evidence = EvidenceSet(
            query=question.question,
            evidence=[
                Evidence(Chunk("chunk-a", "doc-1", "a", None, None, 0), 0.9, 1),
                Evidence(Chunk("chunk-b", "doc-1", "b", None, None, 1), 0.8, 2),
            ],
        )
        result = evaluate_question_retrieval(question, evidence, k=2)
        self.assertEqual(result.question_id, "cq-001")
        self.assertAlmostEqual(result.metrics.recall_at_k, 1.0)
        self.assertEqual(result.retrieved_ids, ("chunk-a", "chunk-b"))
