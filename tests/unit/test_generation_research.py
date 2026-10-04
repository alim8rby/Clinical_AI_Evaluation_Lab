import unittest

from src.evaluation.generation_research import (
    compare_generation_strategies,
    evaluate_generation_case,
    summarize_generation_results,
)
from src.generation.provider import MockGenerationProvider
from src.preprocessing.models import Chunk
from src.retrieval.search import Evidence, EvidenceSet


class GenerationResearchTests(unittest.TestCase):
    def setUp(self):
        chunks = [
            Chunk("c1", "d1", "Depression treatment includes psychological therapy.", None, None, 0),
            Chunk("c2", "d1", "Follow-up should assess response and safety.", None, None, 1),
        ]
        self.evidence = EvidenceSet(
            query="What is depression treatment?",
            evidence=[
                Evidence(chunks[0], 1.0, 1),
                Evidence(chunks[1], 0.5, 2),
            ],
        )
        self.question = type(
            "Question",
            (),
            {
                "question_id": "q1",
                "question": "What is depression treatment?",
                "reference_answer": "Depression treatment includes psychological therapy.",
                "key_concepts": ("psychological therapy",),
                "expected_evidence": ("c1",),
            },
        )()

    def test_case_produces_quality_and_operational_metrics(self):
        result = evaluate_generation_case(
            self.question,
            self.evidence,
            MockGenerationProvider(),
            prompt_version="v1",
        )
        self.assertEqual(result.model, "mock-v1")
        self.assertGreaterEqual(result.answer_metrics.correctness, 0.0)
        self.assertGreaterEqual(result.grounding_metrics.faithfulness, 0.0)
        self.assertGreaterEqual(result.reliability_metrics.uncertainty_handling, 0.0)
        self.assertGreaterEqual(result.latency_ms, 0.0)

    def test_summary_aggregates_fixed_strategy(self):
        result = evaluate_generation_case(
            self.question,
            self.evidence,
            MockGenerationProvider(),
            prompt_version="v1",
        )
        summary = summarize_generation_results([result])
        self.assertEqual(summary.model, "mock-v1")
        self.assertEqual(summary.question_count, 1)
        self.assertEqual(summary.total_input_tokens, 0)
        self.assertEqual(summary.total_cost, 0)

    def test_comparison_keeps_conditions_explicit(self):
        comparison = compare_generation_strategies(
            [self.question],
            {"q1": self.evidence},
            {"mock": MockGenerationProvider()},
            benchmark_version="ClinicalQA-v2",
            prompt_version="v1",
        )
        self.assertEqual(comparison.benchmark_version, "ClinicalQA-v2")
        self.assertEqual(comparison.question_count, 1)
        self.assertEqual(comparison.summaries[0].model, "mock-v1")


if __name__ == "__main__":
    unittest.main()
