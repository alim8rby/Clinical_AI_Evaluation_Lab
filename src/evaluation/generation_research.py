"""Controlled generation experiments over fixed evidence."""

from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter
from typing import Protocol

from src.evaluation.answer import evaluate_question_answer
from src.evaluation.benchmark_v2 import BenchmarkV2Question
from src.evaluation.grounding import evaluate_answer_grounding
from src.evaluation.reliability import evaluate_answer_reliability
from src.generation.citations import build_citations
from src.generation.models import Answer
from src.retrieval.search import EvidenceSet


class GenerationProvider(Protocol):
    model: str

    def generate(self, question: str, evidence: EvidenceSet, *, prompt_version: str) -> Answer:
        ...


@dataclass(frozen=True)
class GenerationCaseResult:
    question_id: str
    model: str
    prompt_version: str
    answer_metrics: object
    grounding_metrics: object
    reliability_metrics: object
    latency_ms: float
    input_tokens: int | None
    output_tokens: int | None
    cost: float | None


@dataclass(frozen=True)
class GenerationStrategySummary:
    model: str
    prompt_version: str
    question_count: int
    mean_correctness: float
    mean_completeness: float
    mean_relevance: float
    mean_grounding: float
    mean_unsupported_claim_rate: float
    mean_hallucination_rate: float
    mean_uncertainty_handling: float
    mean_latency_ms: float
    total_input_tokens: int
    total_output_tokens: int
    total_cost: float


def evaluate_generation_case(
    question: BenchmarkV2Question,
    evidence: EvidenceSet,
    provider: GenerationProvider,
    *,
    prompt_version: str,
    semantic_evaluator=None,
    answer_id: str | None = None,
) -> GenerationCaseResult:
    if not evidence.evidence:
        raise ValueError("evidence must not be empty")
    if not prompt_version.strip():
        raise ValueError("prompt_version must not be empty")

    start = perf_counter()
    answer = provider.generate(question.question, evidence, prompt_version=prompt_version)
    latency_ms = (perf_counter() - start) * 1000
    usage = getattr(provider, "last_usage", {})

    resolved_answer_id = answer_id or f"generation_{question.question_id}_{provider.model}"
    citations = build_citations(resolved_answer_id, answer, evidence)
    answer_eval = evaluate_question_answer(question, answer, semantic_evaluator)
    grounding_eval = evaluate_answer_grounding(
        resolved_answer_id, answer, citations, evidence, semantic_evaluator
    )
    reliability_eval = evaluate_answer_reliability(
        resolved_answer_id, answer, grounding_eval.metrics
    )

    return GenerationCaseResult(
        question_id=question.question_id,
        model=answer.model,
        prompt_version=prompt_version,
        answer_metrics=answer_eval.metrics,
        grounding_metrics=grounding_eval.metrics,
        reliability_metrics=reliability_eval.metrics,
        latency_ms=latency_ms,
        input_tokens=usage.get("input_tokens"),
        output_tokens=usage.get("output_tokens"),
        cost=usage.get("cost"),
    )


def summarize_generation_results(
    results: list[GenerationCaseResult],
) -> GenerationStrategySummary:
    if not results:
        raise ValueError("results must not be empty")
    model = results[0].model
    prompt_version = results[0].prompt_version
    if any(r.model != model or r.prompt_version != prompt_version for r in results):
        raise ValueError("results must contain one model and prompt version")

    count = len(results)

    def mean(values):
        return sum(values) / count

    def total_optional(values):
        return sum(value or 0 for value in values)

    return GenerationStrategySummary(
        model=model,
        prompt_version=prompt_version,
        question_count=count,
        mean_correctness=mean([r.answer_metrics.correctness for r in results]),
        mean_completeness=mean([r.answer_metrics.completeness for r in results]),
        mean_relevance=mean([r.answer_metrics.relevance for r in results]),
        mean_grounding=mean([r.grounding_metrics.faithfulness for r in results]),
        mean_unsupported_claim_rate=mean(
            [r.grounding_metrics.unsupported_claim_rate for r in results]
        ),
        mean_hallucination_rate=mean(
            [r.reliability_metrics.hallucination_rate for r in results]
        ),
        mean_uncertainty_handling=mean(
            [r.reliability_metrics.uncertainty_handling for r in results]
        ),
        mean_latency_ms=mean([r.latency_ms for r in results]),
        total_input_tokens=total_optional([r.input_tokens for r in results]),
        total_output_tokens=total_optional([r.output_tokens for r in results]),
        total_cost=total_optional([r.cost for r in results]),
    )


@dataclass(frozen=True)
class GenerationComparison:
    benchmark_version: str
    prompt_version: str
    question_count: int
    summaries: tuple[GenerationStrategySummary, ...]


def compare_generation_strategies(
    questions: list[BenchmarkV2Question],
    evidence_by_question: dict[str, EvidenceSet],
    providers: dict[str, GenerationProvider],
    *,
    benchmark_version: str,
    prompt_version: str,
    semantic_evaluator=None,
) -> GenerationComparison:
    if not questions:
        raise ValueError("questions must not be empty")
    if not evidence_by_question:
        raise ValueError("evidence_by_question must not be empty")
    if not providers:
        raise ValueError("providers must not be empty")
    if not benchmark_version.strip() or not prompt_version.strip():
        raise ValueError("benchmark_version and prompt_version must not be empty")

    summaries = []
    for name, provider in sorted(providers.items()):
        if not name.strip():
            raise ValueError("provider name must not be empty")
        results = [
            evaluate_generation_case(
                question,
                evidence_by_question[question.question_id],
                provider,
                prompt_version=prompt_version,
                semantic_evaluator=semantic_evaluator,
            )
            for question in questions
        ]
        summaries.append(summarize_generation_results(results))

    return GenerationComparison(
        benchmark_version=benchmark_version,
        prompt_version=prompt_version,
        question_count=len(questions),
        summaries=tuple(summaries),
    )
