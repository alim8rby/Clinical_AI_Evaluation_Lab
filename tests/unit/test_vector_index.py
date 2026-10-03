import tempfile
import unittest
from pathlib import Path
from src.ingestion import ingest_document
from src.preprocessing import chunk_document
from src.retrieval import VectorIndex, embed_text

class VectorIndexTests(unittest.TestCase):
    def setUp(self):
        document = ingest_document(title="Guideline", source="Publisher", organization="Org", publication_date=None, url="https://example.org/guideline", content="Depression treatment evidence.\n\nPsychotherapy evidence.").document
        self.chunks = chunk_document(document, max_chars=100)

    def test_embedding_is_normalized_and_deterministic(self):
        first = embed_text("depression treatment evidence")
        second = embed_text("depression treatment evidence")
        self.assertEqual(first, second)
        self.assertAlmostEqual(sum(x*x for x in first) ** 0.5, 1.0)

    def test_index_round_trips_chunks_and_vectors(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "index.json"
            index = VectorIndex(path)
            index.add(self.chunks)
            index.save()
            restored = VectorIndex(path)
            restored.load()
            self.assertEqual(restored.size, len(self.chunks))
            self.assertEqual(restored._items[self.chunks[0].chunk_id].chunk.document_id, self.chunks[0].document_id)

if __name__ == "__main__":
    unittest.main()
