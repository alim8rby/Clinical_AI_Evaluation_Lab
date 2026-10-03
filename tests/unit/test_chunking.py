from datetime import date
import unittest
from src.ingestion import ingest_document
from src.preprocessing import PreprocessingError, chunk_document

class ChunkingTests(unittest.TestCase):
    def setUp(self):
        self.document = ingest_document(
            title="Depression guideline",
            source="Guideline publisher",
            organization="Authoritative Organization",
            publication_date=date(2025, 1, 15),
            url="https://example.org/depression-guideline",
            content="First paragraph.\n\nSecond paragraph with clinical evidence.",
        ).document

    def test_chunks_preserve_provenance_and_order(self):
        chunks = chunk_document(self.document, max_chars=40)
        self.assertGreater(len(chunks), 1)
        self.assertEqual([c.chunk_index for c in chunks], list(range(len(chunks))))
        self.assertTrue(all(c.document_id == self.document.document_id for c in chunks))
        self.assertTrue(all(c.text for c in chunks))
        self.assertTrue(all(c.section is None and c.page is None for c in chunks))

    def test_chunk_ids_are_deterministic(self):
        first = chunk_document(self.document, max_chars=40)
        second = chunk_document(self.document, max_chars=40)
        self.assertEqual([c.chunk_id for c in first], [c.chunk_id for c in second])

    def test_oversized_text_respects_limit(self):
        chunks = chunk_document(self.document, max_chars=20)
        self.assertTrue(all(len(c.text) <= 20 for c in chunks))

    def test_invalid_chunk_size_is_rejected(self):
        with self.assertRaises(PreprocessingError):
            chunk_document(self.document, max_chars=0)

if __name__ == "__main__":
    unittest.main()
