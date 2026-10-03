import tempfile
import unittest
from pathlib import Path

from src.ingestion import ingest_document
from src.preprocessing import chunk_document
from src.retrieval import VectorIndex, retrieve


class RetrievalTests(unittest.TestCase):
    def setUp(self):
        document = ingest_document(
            title="Depression guideline",
            source="Publisher",
            organization="Organization",
            publication_date=None,
            url="https://example.org/depression",
            content=(
                "Depression psychotherapy treatment evidence.\n\n"
                "Medication treatment evidence for depression.\n\n"
                "Unrelated weather information."
            ),
        ).document
        chunks = chunk_document(document, max_chars=200)
        self.index = VectorIndex(Path(tempfile.gettempdir()) / "caiel-test-index.json")
        self.index.add(chunks)

    def test_retrieval_returns_ranked_traceable_evidence(self):
        result = retrieve(self.index, "depression psychotherapy", top_k=2)

        self.assertEqual(result.query, "depression psychotherapy")
        self.assertEqual([item.rank for item in result.evidence], [1, 2])
        self.assertLessEqual(len(result.evidence), 2)
        self.assertTrue(all(item.chunk.document_id for item in result.evidence))
        self.assertTrue(all(item.score >= 0 for item in result.evidence))

    def test_top_k_and_invalid_queries_are_enforced(self):
        self.assertEqual(len(retrieve(self.index, "depression", top_k=1).evidence), 1)
        with self.assertRaises(ValueError):
            retrieve(self.index, "   ")
        with self.assertRaises(ValueError):
            retrieve(self.index, "depression", top_k=0)


if __name__ == "__main__":
    unittest.main()
