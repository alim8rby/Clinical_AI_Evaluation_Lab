import unittest

from src.generation import MockGenerationProvider
from src.generation.citations import CitationError
from src.generation.models import Answer, Claim
from src.ingestion import ingest_document
from src.pipeline import ClinicalRAG
from src.retrieval import EvidenceSet, VectorIndex


def _document():
    return ingest_document(
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


class InvalidCitationProvider:
    model = "invalid-citation-test"

    def generate(self, question, evidence, *, prompt_version):
        return Answer(
            answer_text="Unsupported claim.",
            claims=[Claim(text="Unsupported claim.", citation_indices=[99])],
            uncertainty="Test provider.",
            model=self.model,
            prompt_version=prompt_version,
        )


class RAGPipelineTests(unittest.TestCase):
    def _pipeline(self, generator=None):
        return ClinicalRAG(
            VectorIndex("data/results/integration-index.json"),
            generator or MockGenerationProvider(),
        )

    def test_full_pipeline_produces_traceable_answer(self):
        pipeline = self._pipeline()
        chunks = pipeline.ingest(_document(), max_chars=120)
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

    def test_empty_question_is_rejected(self):
        pipeline = self._pipeline()
        pipeline.ingest(_document())
        with self.assertRaises(ValueError):
            pipeline.ask("   ")

    def test_invalid_top_k_is_rejected(self):
        pipeline = self._pipeline()
        pipeline.ingest(_document())
        with self.assertRaises(ValueError):
            pipeline.ask("What is depression?", top_k=0)

    def test_empty_index_cannot_generate_an_answer(self):
        pipeline = self._pipeline()
        with self.assertRaises(ValueError):
            pipeline.ask("What is depression?")

    def test_invalid_provider_citation_is_rejected(self):
        pipeline = self._pipeline(InvalidCitationProvider())
        pipeline.ingest(_document())
        with self.assertRaises(CitationError):
            pipeline.ask("What is depression?")


if __name__ == "__main__":
    unittest.main()
