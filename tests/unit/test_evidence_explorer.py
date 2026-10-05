import unittest

from src.evidence_explorer.models import (
    ExplorerCitation,
    ExplorerChunk,
    ExplorerDocument,
    build_explorer,
)


class EvidenceExplorerTests(unittest.TestCase):
    def test_marks_retrieved_but_unused_chunks(self):
        explorer = build_explorer(
            run_id="run-1",
            question_id="cq-001",
            question="Question",
            answer_id="answer-1",
            answer_text="Answer",
            uncertainty=None,
            raw_claims=[{"text": "Claim", "citation_indices": [0]}],
            citations=[
                ExplorerCitation("cit-1", 0, "chunk-used", "support"),
            ],
            chunks=[
                ExplorerChunk("chunk-unused", "doc-1", "Unused", None, None, 2, 0.2, False),
                ExplorerChunk("chunk-used", "doc-1", "Used", None, None, 1, 0.9, True),
            ],
            documents=[
                ExplorerDocument("doc-1", "Document", "source", "org", None, "https://example.test"),
            ],
        )
        self.assertTrue(explorer.chunks[1].used_in_citation)
        self.assertFalse(explorer.chunks[0].used_in_citation)

    def test_claims_resolve_to_citations(self):
        explorer = build_explorer(
            run_id="run-1",
            question_id="cq-001",
            question=None,
            answer_id="answer-1",
            answer_text="Answer",
            uncertainty=None,
            raw_claims=[
                {"text": "Claim 0", "citation_indices": [0]},
                {"text": "Claim 1", "citation_indices": []},
            ],
            citations=[
                ExplorerCitation("cit-1", 0, "chunk-1", "support"),
            ],
            chunks=[],
            documents=[],
        )
        self.assertEqual(explorer.claims[0].citations[0].chunk_id, "chunk-1")
        self.assertEqual(explorer.claims[1].citations, ())

    def test_trace_order_is_deterministic(self):
        explorer = build_explorer(
            run_id="run-1",
            question_id="cq-001",
            question=None,
            answer_id=None,
            answer_text=None,
            uncertainty=None,
            raw_claims=[],
            citations=[],
            chunks=[
                ExplorerChunk("chunk-2", "doc-2", "B", None, None, 2, None, False),
                ExplorerChunk("chunk-1", "doc-1", "A", None, None, 1, None, False),
            ],
            documents=[
                ExplorerDocument("doc-2", "B", "s", "o", None, "u"),
                ExplorerDocument("doc-1", "A", "s", "o", None, "u"),
            ],
        )
        self.assertEqual([x.chunk_id for x in explorer.chunks], ["chunk-1", "chunk-2"])
        self.assertEqual([x.document_id for x in explorer.documents], ["doc-1", "doc-2"])


if __name__ == "__main__":
    unittest.main()
