# V2.1 ClinicalQA-v1 Benchmark

## Purpose

ClinicalQA-v1 is the controlled benchmark for evaluating the V1 depression RAG system.

The initial seed contains eight questions across easy, medium, and hard difficulty. It is an engineering seed, not a validated or statistically representative clinical benchmark.

## Evidence gate

Every expected evidence item must eventually resolve to a real chunk in the controlled knowledge base.

The validator exposes two states:

- **Schema-valid:** question structure and values are valid.
- **Evaluation-ready:** every expected evidence ID resolves to an available controlled chunk.

The current seed intentionally uses DEFERRED_TO_CONTROLLED_CORPUS because V1 does not yet contain a frozen clinical corpus. This marker is always treated as unresolved.

Retrieval metrics must not run against unresolved questions.

## Evidence mapping rule

Expected evidence should contain stable chunk_id values produced by the V1 preprocessing pipeline. Do not store free-text excerpts as the canonical identifier.

When the controlled corpus is frozen:

1. ingest authoritative documents;
2. preprocess them into chunks;
3. freeze the resulting chunk IDs;
4. map each benchmark question to one or more supporting chunk IDs;
5. run the evidence gate;
6. only then use the benchmark for retrieval evaluation.

## Growth plan

- Seed: 30–50 questions
- Target: 100–300 questions

The benchmark should grow only after the evaluation pipeline and evidence mapping rules are stable.

## Freeze rule

Do not silently change existing question meaning, reference answers, or evidence mappings. Changes that affect evaluation results require a new benchmark version.
