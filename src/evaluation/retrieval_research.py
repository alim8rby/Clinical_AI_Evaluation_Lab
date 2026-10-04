"""Controlled retrieval-strategy experiments for V5.3."""

from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter
from typing import Protocol

from src.evaluation.benchmark_v2 import BenchmarkV2Question
from src.evaluation.retrieval_metrics import RetrievalMetrics, evaluate_retrieval
from src.preprocessing.models import Chunk
from src.retrieval.bm25 import BM25Retriever
from src.retrieval.embeddings import embed_text
from src.retrieval.hybrid import HybridRetriever
from src.retrieval.search import EvidenceSet, _cosine


class ResearchRetriever(Protocol):
    def retrieve(self, query: str, *, top_k: int = 5) -> EvidenceSet:
        """Retrieve ranked evidence for one query."""


class DenseResearchRetriever:
    """Deterministic dense baseline using the V1 hashed embedding."""

    name = "dense"

    def __init__(self, chunks: list[Chunk], *, dimensions: int = 256):
        if not chunks:
            raise ValueError("chunks must not be empty")
        if dimensions <= 0:
            raise ValueError("dimensions must be greater than zero")
        self.chunks = tuple(chunks)
        self.dimensions = dimensions
        self.vectors = {
            chunk.chunk_id: embed_text(chunk.text, dimensions=dimensions)
            for chunk in self.chunks
        }

    def retrieve(self, query: str, *, top_k: int = 5) -> EvidenceSet:
        if not query.strip():
            raise ValueError("query must not be empty")
        if top_k <= 0:
            raise ValueError("top_k must be greater than zero")
        query_vector = embed_text(query, dimensions=self.dimensions)
        scored = [
            (chunk, _cosine(query_vector, self.vectors[chunk.chunk_id]))
            for chunk in self.chunks
        ]
        scored.sort(key=lambda item: (-item[1], item[0].chunk_id))
        from src.retrieval.search import Evidence

        return EvidenceSet(
            query=query,
            evidence=[
                Evidence(chunk=chunk, score=score, rank=rank)
                for rank, (chunk, score) in enumerate(scored[:top_k], start=1)
            ],
        )


@dataclass(frozen=True)
class RetrievalCaseResult:
    question_id: str
    strategy: str
    metrics: RetrievalMetrics
    latency_ms: float


@dataclass(frozen=True)
class RetrievalStrategySummary:
    strategy: str
    question_count: int
    mean_precision_at_k: float
    mean_recall_at_k: float
    mean_mrr: float
    mean_ndcg: float
    mean_latency_ms: float


def evaluate_retrieval_strategy(
    questions: list[BenchmarkV2Question],
    retriever: ResearchRetriever,
    *,
    strategy: str,
    top_k: int = 5,
) -> list[RetrievalCaseResult]:
    if not questions:
        raise ValueError("questions must not be empty")
    if not strategy.strip():
        raise ValueError("strategy must not be empty")
    if top_k <= 0:
        raise ValueError("top_k must be greater than zero")

    results = []
    for question in questions:
        start = perf_counter()
        evidence = retriever.retrieve(question.question, top_k=top_k)
        latency_ms = (perf_counter() - start) * 1000
        retrieved_ids = [item.chunk.chunk_id for item in evidence.evidence]
        metrics = evaluate_retrieval(
            retrieved_ids,
            set(question.expected_evidence),
            k=top_k,
        )
        results.append(
            RetrievalCaseResult(
                question_id=question.question_id,
                strategy=strategy,
                metrics=metrics,
                latency_ms=latency_ms,
            )
        )
    return results


def summarize_retrieval_results(
    results: list[RetrievalCaseResult],
) -> RetrievalStrategySummary:
    if not results:
        raise ValueError("results must not be empty")
    strategy = results[0].strategy
    if any(result.strategy != strategy for result in results):
        raise ValueError("results must contain one strategy")

    count = len(results)
    return RetrievalStrategySummary(
        strategy=strategy,
        question_count=count,
        mean_precision_at_k=sum(r.metrics.precision_at_k for r in results) / count,
        mean_recall_at_k=sum(r.metrics.recall_at_k for r in results) / count,
        mean_mrr=sum(r.metrics.mrr for r in results) / count,
        mean_ndcg=sum(r.metrics.ndcg for r in results) / count,
        mean_latency_ms=sum(r.latency_ms for r in results) / count,
    )


def build_research_retrievers(
    chunks: list[Chunk],
    *,
    hybrid_alpha: float = 0.5,
) -> dict[str, ResearchRetriever]:
    return {
        "dense": DenseResearchRetriever(chunks),
        "bm25": BM25Retriever(chunks),
        "hybrid": HybridRetriever(chunks, alpha=hybrid_alpha),
    }


@dataclass(frozen=True)
class RetrievalResearchReport:
    benchmark_version: str
    top_k: int
    summaries: tuple[RetrievalStrategySummary, ...]


def compare_retrieval_strategies(
    questions: list[BenchmarkV2Question],
    retrievers: dict[str, ResearchRetriever],
    *,
    benchmark_version: str,
    top_k: int = 5,
) -> RetrievalResearchReport:
    if not benchmark_version.strip():
        raise ValueError("benchmark_version must not be empty")
    if not retrievers:
        raise ValueError("retrievers must not be empty")
    summaries = []
    for strategy, retriever in sorted(retrievers.items()):
        results = evaluate_retrieval_strategy(
            questions, retriever, strategy=strategy, top_k=top_k
        )
        summaries.append(summarize_retrieval_results(results))
    return RetrievalResearchReport(
        benchmark_version=benchmark_version,
        top_k=top_k,
        summaries=tuple(summaries),
    )
