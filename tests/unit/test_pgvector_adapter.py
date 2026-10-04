import unittest
from unittest.mock import Mock
from src.retrieval.pgvector import PgVectorRetriever
from src.retrieval.provider import LocalHashedEmbeddingProvider

class PgVectorAdapterTests(unittest.TestCase):
    def test_empty_query_rejected(self):
        with self.assertRaises(ValueError):
            PgVectorRetriever(Mock(), LocalHashedEmbeddingProvider()).retrieve("")

    def test_invalid_top_k_rejected(self):
        with self.assertRaises(ValueError):
            PgVectorRetriever(Mock(), LocalHashedEmbeddingProvider()).retrieve("depression", top_k=0)

    def test_provider_dimension_is_used(self):
        provider = LocalHashedEmbeddingProvider(dimensions=8)
        self.assertEqual(provider.dimensions, 8)

if __name__ == "__main__":
    unittest.main()
