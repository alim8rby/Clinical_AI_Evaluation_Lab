import unittest

from src.generation import MockGenerationProvider
from src.ingestion import ingest_document
from src.pipeline import ClinicalRAG
from src.retrieval import VectorIndex


class RAGPipelineTests(unittest.TestCase):
    def test_full_pipeline_produces_traceable_answer(self):
        document = ingest_document(
            title="Depression guideline",
            source="Publisher",
            organization="Organization",
            publication_date=None,
            url="https://example.org/depression",
            content=(
                "Psychotherapy is an evidence-based treatment for depression.\n\n"
                "Medication is another treatment option."
            ),
        ).document

        pipeline = ClinicalRAG(
            VectorIndex("data/results/integration-index.json"),
            MockGenerationProvider(),
        )
        chunks = pipeline.ingest(document, max_chars=120)
        result = pipeline.ask(
            "What evidence is available for depression treatment?",
            top_k=2,
            answer_id="answer-integration-1",
        )

        self.assertGreaterEqual(len(chunks), 1)
        self.assertGreaterEqual(len(result.evidence.evidence), 1)
        self.assertTrue(result.answer.answer_text)
        self.assertEqual(len(result.citations), len(result.answer.claims))
        self.assertTrue(
            all(
                citation.chunk_id in {chunk.chunk_id for chunk in result.chunks}
                for citation in result.citations
            )
        )


if __name__ == "__main__":
    unittest.main()
