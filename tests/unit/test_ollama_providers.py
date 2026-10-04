import unittest
from unittest.mock import patch, Mock

from src.generation.ollama import OllamaGenerationProvider
from src.retrieval.ollama import OllamaEmbeddingProvider


class OllamaProviderTests(unittest.TestCase):
    @patch("src.generation.ollama.httpx.post")
    def test_generation_maps_structured_response(self, post):
        response = Mock()
        response.raise_for_status.return_value = None
        response.json.return_value = {
            "response": '{"answer_text":"Evidence-based answer.","uncertainty":"limited","claims":[{"text":"Claim","citation_indices":[1]}]}'
        }
        post.return_value = response

        from src.retrieval.search import EvidenceSet, Evidence
        from src.preprocessing.models import Chunk
        evidence = EvidenceSet("question", [Evidence(Chunk("c1","d1","evidence",None,None,0), 1.0, 1)])
        answer = OllamaGenerationProvider().generate("question", evidence, prompt_version="v1")
        self.assertEqual(answer.model, "llama3.2:3b")
        self.assertEqual(answer.claims[0].citation_indices, [1])

    @patch("src.retrieval.ollama.httpx.post")
    def test_embedding_maps_vector(self, post):
        response = Mock()
        response.raise_for_status.return_value = None
        response.json.return_value = {"embeddings": [[0.1, 0.2, 0.3]]}
        post.return_value = response
        provider = OllamaEmbeddingProvider()
        self.assertEqual(provider.embed("hello"), [0.1, 0.2, 0.3])
        self.assertEqual(provider.dimensions, 3)

if __name__ == "__main__":
    unittest.main()
