import json
import unittest
from pathlib import Path

from src.evaluation.benchmark_v2 import validate_benchmark_v2_payload
from src.evaluation.retrieval_research import (
    build_research_retrievers,
    compare_retrieval_strategies,
    evaluate_retrieval_strategy,
    summarize_retrieval_results,
)
from src.ingestion.models import SourceDocument
from src.preprocessing.chunk import chunk_document


ROOT = Path(__file__).parents[2]


class RetrievalResearchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sources = json.loads(
            (ROOT / "data/raw/controlled/depression_sources.json").read_text(encoding="utf-8")
        )
        cls.chunks = []
        for source in sources:
            cls.chunks.extend(chunk_document(SourceDocument(**source)))

        payload = json.loads(
            (ROOT / "data/benchmark/clinicalqa_v2.json").read_text(encoding="utf-8")
        )
        cls.questions = validate_benchmark_v2_payload(payload)

    def test_builds_three_controlled_strategies(self):
        retrievers = build_research_retrievers(self.chunks)
        self.assertEqual(set(retrievers), {"dense", "bm25", "hybrid"})

    def test_each_strategy_returns_valid_benchmark_metrics(self):
        retrievers = build_research_retrievers(self.chunks)
        sample = self.questions[:5]
        for name, retriever in retrievers.items():
            results = evaluate_retrieval_strategy(
                sample, retriever, strategy=name, top_k=5
            )
            self.assertEqual(len(results), 5)
            self.assertTrue(all(r.metrics.k == 5 for r in results))
            summary = summarize_retrieval_results(results)
            self.assertEqual(summary.strategy, name)
            self.assertEqual(summary.question_count, 5)
            self.assertGreaterEqual(summary.mean_recall_at_k, 0.0)
            self.assertLessEqual(summary.mean_recall_at_k, 1.0)
            self.assertGreaterEqual(summary.mean_latency_ms, 0.0)

    def test_strategy_results_are_deterministic_for_fixed_corpus(self):
        retrievers = build_research_retrievers(self.chunks)
        first = evaluate_retrieval_strategy(
            self.questions[:3], retrievers["bm25"], strategy="bm25", top_k=5
        )
        second = evaluate_retrieval_strategy(
            self.questions[:3], retrievers["bm25"], strategy="bm25", top_k=5
        )
        self.assertEqual(
            [r.metrics for r in first],
            [r.metrics for r in second],
        )


if __name__ == "__main__":
    unittest.main()

    def test_comparison_report_contains_all_strategies(self):
        report = compare_retrieval_strategies(
            self.questions[:3],
            build_research_retrievers(self.chunks),
            benchmark_version="ClinicalQA-v2",
            top_k=5,
        )
        self.assertEqual(report.benchmark_version, "ClinicalQA-v2")
        self.assertEqual(report.top_k, 5)
        self.assertEqual({item.strategy for item in report.summaries}, {"bm25", "dense", "hybrid"})
