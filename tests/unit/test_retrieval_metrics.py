import unittest

from src.evaluation.retrieval_metrics import (
    evaluate_retrieval,
    ndcg_at_k,
    precision_at_k,
    recall_at_k,
    reciprocal_rank,
)


class RetrievalMetricTests(unittest.TestCase):
    def test_precision_at_k(self):
        self.assertAlmostEqual(precision_at_k(["a", "b", "c", "d"], {"b", "d"}, 4), 0.5)
        self.assertAlmostEqual(precision_at_k(["a", "b", "c", "d"], {"b", "d"}, 2), 0.5)

    def test_recall_at_k(self):
        self.assertAlmostEqual(recall_at_k(["a", "b", "c", "d"], {"b", "d"}, 2), 0.5)
        self.assertAlmostEqual(recall_at_k(["a", "b", "c", "d"], {"b", "d"}, 4), 1.0)

    def test_mrr(self):
        self.assertAlmostEqual(reciprocal_rank(["x", "b", "a"], {"b"}, 3), 0.5)
        self.assertEqual(reciprocal_rank(["x", "y"], {"b"}, 2), 0.0)

    def test_ndcg(self):
        self.assertAlmostEqual(ndcg_at_k(["b", "a", "c"], {"b"}, 3), 1.0)
        self.assertLess(ndcg_at_k(["a", "b", "c"], {"b"}, 3), 1.0)

    def test_aggregate_result(self):
        result = evaluate_retrieval(["a", "b", "c"], {"b", "c"}, k=3)
        self.assertEqual(result.k, 3)
        self.assertEqual(result.retrieved_count, 3)
        self.assertEqual(result.expected_count, 2)
        self.assertAlmostEqual(result.precision_at_k, 2 / 3)
        self.assertAlmostEqual(result.recall_at_k, 1.0)
        self.assertAlmostEqual(result.mrr, 0.5)

    def test_rejects_empty_expected(self):
        with self.assertRaises(ValueError):
            precision_at_k(["a"], set(), 1)

    def test_rejects_duplicate_retrieval(self):
        with self.assertRaises(ValueError):
            recall_at_k(["a", "a"], {"a"}, 2)

    def test_rejects_invalid_k(self):
        with self.assertRaises(ValueError):
            ndcg_at_k(["a"], {"a"}, 0)
