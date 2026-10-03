from datetime import date
from pathlib import Path
import tempfile
import unittest

from src.ingestion import IngestionError, ingest_document, ingest_text_file


class IngestionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.metadata = {
            "title": "Depression guideline",
            "source": "Guideline publisher",
            "organization": "Authoritative Organization",
            "publication_date": date(2025, 1, 15),
            "url": "https://example.org/depression-guideline",
        }

    def test_ingest_normalizes_content_and_creates_stable_id(self) -> None:
        result = ingest_document(
            content="  First line  \r\n\r\n\r\nSecond   line  ",
            **self.metadata,
        )

        self.assertEqual(result.document.content, "First line\n\nSecond line")
        self.assertTrue(result.document.document_id.startswith("doc_"))

        repeat = ingest_document(content="First line\n\nSecond line", **self.metadata)
        self.assertEqual(result.document.document_id, repeat.document.document_id)

    def test_ingest_preserves_provenance_metadata(self) -> None:
        result = ingest_document(content="Clinical content", **self.metadata)

        self.assertEqual(result.document.title, self.metadata["title"])
        self.assertEqual(result.document.source, self.metadata["source"])
        self.assertEqual(result.document.organization, self.metadata["organization"])
        self.assertEqual(result.document.publication_date, self.metadata["publication_date"])
        self.assertEqual(result.document.url, self.metadata["url"])

    def test_invalid_metadata_or_content_is_rejected(self) -> None:
        with self.assertRaises(IngestionError):
            ingest_document(content="content", **{**self.metadata, "title": "   "})
        with self.assertRaises(IngestionError):
            ingest_document(content="content", **{**self.metadata, "url": "not-a-url"})
        with self.assertRaises(IngestionError):
            ingest_document(content="   ", **self.metadata)

    def test_text_file_ingestion_uses_same_contract(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "source.txt"
            path.write_text("Guideline content", encoding="utf-8")

            result = ingest_text_file(path, **self.metadata)

            self.assertEqual(result.document.content, "Guideline content")
            self.assertEqual(result.source_path, str(path))


if __name__ == "__main__":
    unittest.main()
