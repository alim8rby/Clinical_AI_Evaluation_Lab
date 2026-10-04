# V2.1 ClinicalQA-v1 Benchmark

## Purpose

ClinicalQA-v1 is the controlled benchmark for evaluating the V1 depression RAG system.

The initial seed contains eight questions across easy, medium, and hard difficulty. It is an engineering seed, not a validated or statistically representative clinical benchmark.

## Evidence status

The seed questions currently use DEFERRED_TO_CONTROLLED_CORPUS as a temporary evidence marker. Expected evidence must resolve to chunks in the controlled knowledge base before the benchmark is used for retrieval scoring.

V2.1 therefore has two gates:

1. Schema gate: benchmark structure is valid.
2. Evidence gate: expected evidence resolves to controlled chunks.

Only the second gate makes a question ready for retrieval evaluation.

## Growth plan

- Seed: 30–50 questions
- Target: 100–300 questions

The benchmark should grow only after the evaluation pipeline and evidence mapping rules are stable.

## Freeze rule

Do not silently change existing question meaning, reference answers, or evidence mappings. Changes that affect evaluation results require a new benchmark version.
