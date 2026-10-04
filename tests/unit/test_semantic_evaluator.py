import unittest
from unittest.mock import Mock, patch

from src.evaluation.ollama_semantic import OllamaSemanticEvaluator


class SemanticEvaluatorTests(unittest.TestCase):
    @patch("src.evaluation.ollama_semantic.httpx.post")
    def test_answer_scores_are_structured_and_bounded(self, post):
        response = Mock()
        response.raise_for_status.return_value = None
        response.json.return_value = {
            "response": '{"correctness":0.9,"completeness":0.8,"relevance":0.95}'
        }
        post.return_value = response
        scores = OllamaSemanticEvaluator().evaluate_answer(
            question="What is depression?",
            reference_answer="A depressive disorder is characterized by persistent low mood.",
            key_concepts=["low mood"],
            answer_text="Depression involves persistent low mood.",
        )
        self.assertEqual(scores, {"correctness": 0.9, "completeness": 0.8, "relevance": 0.95})

    @patch("src.evaluation.ollama_semantic.httpx.post")
    def test_grounding_scores_are_structured(self, post):
        response = Mock()
        response.raise_for_status.return_value = None
        response.json.return_value = {
            "response": '{"faithfulness":0.75,"unsupported_claim_rate":0.25}'
        }
        post.return_value = response
        scores = OllamaSemanticEvaluator().evaluate_grounding(
            question="question",
            answer_text="answer",
            claims=[{"text": "claim"}],
            evidence=["evidence"],
        )
        self.assertEqual(scores, {"faithfulness": 0.75, "unsupported_claim_rate": 0.25})

    @patch("src.evaluation.ollama_semantic.httpx.post")
    def test_out_of_range_score_rejected(self, post):
        response = Mock()
        response.raise_for_status.return_value = None
        response.json.return_value = {"response": '{"correctness":1.5}'}
        post.return_value = response
        with self.assertRaises(RuntimeError):
            OllamaSemanticEvaluator().evaluate_answer(
                question="q", reference_answer="r", key_concepts=["k"], answer_text="a"
            )
