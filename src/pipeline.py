from dataclasses import dataclass

from src.generation import Answer, Citation, GenerationProvider, build_citations
from src.ingestion.models import SourceDocument
from src.preprocessing import Chunk, chunk_document
from src.retrieval import EvidenceSet, VectorIndex, retrieve


@dataclass(frozen=True)
class RAGResult:
    question: str
    chunks: list[Chunk]
    evidence: EvidenceSet
    answer: Answer
    citations: list[Citation]


class ClinicalRAG:
    """End-to-end V1 pipeline over the existing module contracts."""

    def __init__(self, index: VectorIndex, generator: GenerationProvider):
        self.index = index
        self.generator = generator

    def ingest(self, document: SourceDocument, *, max_chars: int = 1200) -> list[Chunk]:
        chunks = chunk_document(document, max_chars=max_chars)
        self.index.add(chunks)
        return chunks

    def ask(
        self,
        question: str,
        *,
        top_k: int = 5,
        answer_id: str = "answer-1",
        prompt_version: str = "v1",
    ) -> RAGResult:
        evidence = retrieve(self.index, question, top_k=top_k)
        answer = self.generator.generate(
            question,
            evidence,
            prompt_version=prompt_version,
        )
        citations = build_citations(answer, evidence, answer_id=answer_id)
        return RAGResult(
            question=question,
            chunks=[item.chunk for item in evidence.evidence],
            evidence=evidence,
            answer=answer,
            citations=citations,
        )
