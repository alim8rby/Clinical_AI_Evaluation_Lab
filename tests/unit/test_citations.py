import unittest

from src.generation import Answer, Claim, CitationError, build_citations
from src.ingestion import ingest_document
from src.preprocessing import chunk_document
from src.retrieval import VectorIndex, retrieve

class CitationTests(unittest.TestCase):
    def setUp(self):
        document = ingest_document(
            title="Guideline", source="Publisher", organization="Org",
            publication_date=None, url="https://example.org/guideline",
            content="Depression treatment evidence.",
        ).document
        index = VectorIndex("data/results/test-citations.json")
        index.add(chunk_document(document, max_chars=100))
        self.evidence = retrieve(index, "depression treatment", top_k=1)

    def test_citations_resolve_to_retrieved_chunks(self):
        answer = Answer(
            answer_text="Treatment evidence is available.",
            claims=[Claim("Treatment evidence is available.", [1])],
            uncertainty=None, model="mock-v1", prompt_version="v1",
        )
        citations = build_citations(answer, self.evidence, answer_id="answer-1")
        self.assertEqual(len(citations), 1)
        self.assertEqual(citations[0].answer_id, "answer-1")
        self.assertEqual(citations[0].chunk_id, self.evidence.evidence[0].chunk.chunk_id)

    def test_invalid_citation_is_rejected(self):
        answer = Answer(
            answer_text="Unsupported.", claims=[Claim("Unsupported.", [2])],
            uncertainty=None, model="mock-v1", prompt_version="v1",
        )
        with self.assertRaises(CitationError):
            build_citations(answer, self.evidence, answer_id="answer-1")

if __name__ == "__main__":
    unittest.main()
