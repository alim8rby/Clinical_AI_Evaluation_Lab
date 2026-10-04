import unittest

from src.evaluation.answer import evaluate_question_answer
from src.evaluation.benchmark import BenchmarkQuestion
from src.generation.models import Answer


class AnswerEvaluationTests(unittest.TestCase):
    def test_evaluates_generated_answer(self):
        question = BenchmarkQuestion(
            question_id="cq-001",
            question="What is depression?",
            domain="depression",
            difficulty="easy",
            expected_evidence=("chunk-1",),
            reference_answer="Persistent low mood and loss of interest can characterize depression.",
            key_concepts=("low mood", "loss of interest"),
        )
        answer = Answer(
            answer_text="Persistent low mood and loss of interest can characterize depression.",
            claims=[],
            uncertainty="",
            model="mock-v1",
            prompt_version="v1",
        )
        result = evaluate_question_answer(question, answer)
        self.assertEqual(result.question_id, "cq-001")
        self.assertEqual(result.metrics.correctness, 1.0)
        self.assertEqual(result.metrics.completeness, 1.0)
