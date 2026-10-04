# V2.1 ClinicalQA-v1 Benchmark

## Purpose

ClinicalQA-v1 is the controlled benchmark for evaluating the V1 depression RAG system.

The current seed contains eight questions across easy, medium, and hard difficulty. It is an engineering seed, not a validated or statistically representative clinical benchmark.

## Evidence gate

Every expected evidence item must resolve to a real chunk in the controlled knowledge base.

The current controlled corpus resolves all benchmark evidence mappings. Retrieval evaluation is therefore allowed for the current eight-question seed.

## Controlled corpus

The benchmark uses compact evidence snapshots from the World Health Organization and National Institute for Health and Care Excellence. Full copyrighted source documents are not stored.

## Evidence mapping rule

Expected evidence uses stable chunk IDs produced by the V1 preprocessing pipeline. Changes to the controlled corpus that alter chunk IDs require remapping or a new benchmark version.

## Growth plan

- Current seed: 8 questions
- Next expansion: 30–50 questions
- Target: 100–300 questions

## Freeze rule

Do not silently change existing question meaning, reference answers, or evidence mappings. Changes that affect evaluation results require a new benchmark version.
