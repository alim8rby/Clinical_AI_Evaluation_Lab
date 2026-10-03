import unittest

from src.generation import MockGenerationProvider, PROMPT_VERSION, build_prompt
from src.ingestion import ingest_document
from src.preprocessing import chunk_document
from src.retrieval import VectorIndex, retrieve

class GenerationTests(unittest.TestCase):
    def setUp(self):
        document = ingest_document(
            title="Guideline", source="Publisher", organization="Org",
            publication_date=None, url="https://example.org/guideline",
            content="Depression treatment evidence.",
        ).document
        chunks = chunk_document(document, max_chars=100)
        index = VectorIndex("data/results/test-index.json")
        index.add(chunks)
        self.evidence = retrieve(index, "depression treatment", top_k=1)

    def test_mock_generation_returns_structured_grounded_answer(self):
        answer = MockGenerationProvider().generate(
            "What evidence is available?", self.evidence, prompt_version=PROMPT_VERSION
        )
        self.assertTrue(answer.answer_text)
        self.assertEqual(answer.model, "mock-v1")
        self.assertEqual(answer.prompt_version, PROMPT_VERSION)
        self.assertEqual(answer.claims[0].citation_indices, [1])

    def test_prompt_contains_grounding_rules(self):
        prompt = build_prompt("What is depression?", "Evidence chunk")
        self.assertIn("Do not invent facts or citations.", prompt)
        self.assertIn("Evidence chunk", prompt)

if __name__ == "__main__":
    unittest.main()
