# Clinical AI Evaluation Lab

**CAIEL** is a portfolio project for building and evaluating evidence-grounded clinical QA systems.

The goal is not just to make a medical chatbot. The goal is to see **where an AI answer came from, how reliable it is, and where it fails**.

> Portfolio/research project. Not for patient care.

## Current status

**V2 — Evaluation Lab: FROZEN**

V0 architecture and V1 RAG are also frozen. The repository now has a complete local RAG baseline plus a deterministic evaluation layer.

### What is built

Source document → Ingestion → Chunking → Embeddings/vector index → Retrieval → Generation → Citations → ClinicalQA-v1 → Evaluation → Experiments → Comparison + Report

## V1 — Working RAG

- Document ingestion and provenance
- Deterministic document and chunk IDs
- Document chunking
- Local JSON-backed vector index
- Ranked retrieval
- Generation provider interface
- Deterministic mock generator
- Claim-level evidence references
- Citation validation
- End-to-end RAG pipeline
- Unit, integration, and failure-path tests

Traceability: Question → Evidence → Answer → Claim → Citation → Chunk → Document

## V2 — Evaluation Lab

### Benchmark

- ClinicalQA-v1
- Depression only
- Current seed: 8 questions
- Controlled evidence mappings to stable chunk IDs
- Planned growth: 30–50 questions, then 100–300

### Metrics

Retrieval: Precision@K, Recall@K, MRR, nDCG.

Answer quality: Correctness, Completeness, Relevance.

Grounding: Citation coverage, Citation validity, Faithfulness, Unsupported claim rate.

Reliability: Hallucination proxy, Critical-error signal, Uncertainty handling, Unsupported recommendation rate.

### Experiments and reports

Experiments record model, embedding, retriever, top-k, prompt, benchmark, and run metadata. Same-benchmark comparisons expose metric deltas and sample counts with no hidden composite score.

Reports contain experiment identity, benchmark, configuration, sample count, aggregated metrics, and recorded failures.

## V2 audit result

**V2.0–V2.9: COMPLETE AND FROZEN**

The audit repaired the benchmark evidence documentation and added failure retention to ExperimentResult so failures flow directly into reports.

See docs/methodology/v2-audit.md for the freeze record and limitations.

## What is still in progress

### V3 — Failure Observatory — IN PROGRESS

- Failure classification and persistence
- Failure analysis workflows
- Failure Observatory UI
- Regression testing around known failures

### V4 — Productionization — PLANNED

- FastAPI
- PostgreSQL + pgvector
- Structured persistence
- Logging and monitoring
- Docker
- Deployment
- CI/CD

### V5 — Healthcare interoperability — PLANNED

- FHIR
- Provenance
- Structured clinical data
- Human-in-the-loop workflows

## Important limitations

- Benchmark has only eight questions.
- Controlled corpus is compact.
- Answer and grounding evaluation use token-overlap baselines.
- Reliability signals are heuristic.
- No production persistence or UI exists yet.
- No real patient data or autonomous clinical decision-making.
- Local RAG still uses deterministic hashed-token embeddings and a mock generation provider.
- No clinical validation is claimed.

## Documentation

- docs/product-spec.md — product definition
- docs/roadmap.md — roadmap and phase status
- docs/data-model.md — core data model
- docs/failure-taxonomy.md — failure taxonomy
- docs/architecture/ — architecture and contracts
- docs/methodology/ — implementation methodology and audits
- docs/methodology/v2-audit.md — V2 freeze record

## Tech direction

Python · FastAPI · PostgreSQL · pgvector · LLM provider abstraction · Docker · pytest

Production infrastructure is introduced in later phases. V2 remains deliberately local and deterministic.

## License

Project license and contribution guidance will be added before public release.
