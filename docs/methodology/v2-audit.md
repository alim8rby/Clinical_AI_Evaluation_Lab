# V2 Audit and Freeze

## Result

**V2 — Evaluation Lab: FROZEN**

V2.0–V2.9 is complete.

## What was built

- Evaluation architecture and contracts
- ClinicalQA-v1 depression benchmark
- Controlled evidence corpus with stable chunk mappings
- Retrieval metrics: Precision@K, Recall@K, MRR, nDCG
- Answer metrics: correctness, completeness, relevance
- Grounding metrics: citation coverage, citation validity, faithfulness, unsupported claim rate
- Reliability signals: hallucination proxy, critical-error signal, uncertainty handling, unsupported recommendation rate
- Immutable experiment configuration and run records
- Same-benchmark experiment comparison with transparent metric deltas
- Reproducible Markdown evaluation reports
- Unit/integration test coverage for V2 components
- Methodology documentation for each V2 stage

## Audit findings repaired

1. Benchmark documentation incorrectly described evidence mappings as deferred; it now reflects the resolved controlled corpus.
2. ExperimentResult did not retain failures; failures are now recorded in the result and flow into reports.

## Known limitations

- Benchmark size is currently eight questions.
- Evidence corpus is compact and not a complete clinical knowledge base.
- Answer evaluation uses token overlap, not semantic clinical judgement.
- Grounding uses token overlap, not semantic entailment.
- Reliability signals are heuristic, not a clinical safety classifier.
- Results remain in memory; no persistence layer exists.
- No production API, database, frontend, authentication, deployment, or CI/CD exists yet.
- Local test execution was not performed during this audit; repository source and test structure were inspected.

## Freeze rule

Do not add V3/V4 infrastructure to V2. Concrete correctness issues require a documented decision.

## Next phase

V3 starts with the Failure Observatory: structured failure classification, inspection, regression coverage, and later UI.
