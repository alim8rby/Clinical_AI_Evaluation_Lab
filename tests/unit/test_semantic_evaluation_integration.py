import unittest
from unittest.mock import Mock

from src.evaluation.answer import evaluate_question_answer
from src.evaluation.grounding import evaluate_answer_grounding
from src.evaluation.benchmark import BenchmarkQuestion
from src.evaluation.grounding_metrics import GroundingMetrics
from src.generation.citations import Citation
from src.generation.models import Answer, Claim
from src.retrieval.search import Evidence, EvidenceSet
from src.preprocessing.models import Chunk


class SemanticEvaluationIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.question = BenchmarkQuestion(
            question_id="q1",
            question="What is depression?",
            domain="depression",
            difficulty="easy",
            expected_evidence=["c1"],
            reference_answer="Depression involves persistent low mood.",
            key_concepts=["persistent low mood"],
        )
        self.answer = Answer(
            answer_text="Depression involves persistent low mood.",
            claims=(Claim("Depression involves persistent low mood.", (1,)),),
            uncertainty="limited",
            model="mock",
            prompt_version="v1",
        )
        self.evidence = EvidenceSet(
            "What is depression?",
            [Evidence(Chunk("c1", "d1", "Depression involves persistent low mood.", None, None, 0), 1.0, 1)],
        )
        self.citation = Citation("a1-c0-e1", "a1", 1, "c1", "c1")

    def test_semantic_answer_scores_are_added_without_replacing_baselines(self):
        evaluator = Mock()
        evaluator.evaluator_version = "semantic-test-v1"
        evaluator.evaluate_answer.return_value = {
            "correctness": 0.9,
            "completeness": 0.8,
            "relevance": 0.95,
        }
        result = evaluate_question_answer(self.question, self.answer, evaluator)
        self.assertEqual(result.metrics.correctness, 1.0)
        self.assertEqual(result.metrics.semantic_correctness, 0.9)
        self.assertEqual(result.metrics.semantic_completeness, 0.8)
        self.assertEqual(result.metrics.semantic_relevance, 0.95)

    def test_semantic_grounding_scores_are_added_without_replacing_baselines(self):
        evaluator = Mock()
        evaluator.evaluator_version = "semantic-test-v1"
        evaluator.evaluate_grounding.return_value = {
            "faithfulness": 0.9,
            "unsupported_claim_rate": 0.1,
        }
        result = evaluate_answer_grounding("a1", self.answer, [self.citation], self.evidence, evaluator)
        self.assertEqual(result.metrics.faithfulness, 1.0)
        self.assertEqual(result.metrics.semantic_faithfulness, 0.9)
        self.assertEqual(result.metrics.semantic_unsupported_claim_rate, 0.1)


if __name__ == "__main__":
    unittest.main()
