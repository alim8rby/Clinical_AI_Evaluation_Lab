# Clinical AI Evaluation Lab

**CAIEL** is a portfolio project for building and evaluating evidence-grounded clinical QA systems.

The goal is not just to make a medical chatbot. The goal is to see **where an AI answer came from, how reliable it is, and where it fails**.

> Portfolio/research project. Not for patient care.

## Current status

**V5.11 — Research Reports: ENGINEERING COMPLETE**

V0 architecture and V1 RAG are also frozen. The repository now has a complete local RAG baseline, deterministic evaluation layer, local failure-analysis observatory, and durable research-report artifacts.

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
- Current benchmark: 40 questions
- Controlled evidence mappings to stable chunk IDs
- V5.2 target: expand coverage beyond the current compact benchmark

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

## V3 — Failure Observatory

- Deterministic failure classification and severity
- Local structured failure persistence
- Failure analysis and filtering
- Known-failure regression suite
- Failure Observatory query layer and local UI
- End-to-end V2 evaluation → failure workflow

See docs/methodology/v3-audit.md for the V3 freeze record.

### V4 — Productionization

V4.0–V4.15 is frozen. The application has a FastAPI boundary, PostgreSQL persistence, pgvector retrieval, Ollama provider integration, semantic evaluation, failure analysis, observability, an API-backed frontend, containers, and CI/CD.

### V5 — Evaluation Platform

V5.1 engineering is frozen with a human-calibration framework and explicit annotation rubric. V5.2 is frozen with a 60-question ClinicalQA-v2 benchmark while preserving ClinicalQA-v1 as an immutable baseline. V5.3 adds controlled dense, BM25, and hybrid retrieval comparisons. V5.4 adds controlled generation-provider evaluation with quality, grounding, reliability, latency, token, and cost metrics. V5.5 adds reproducible batch experiment execution, configuration capture, aggregate reporting, and failure retention. V5.6 adds paired statistical comparisons, deterministic bootstrap confidence intervals, and effect-size reporting. V5.7 adds experiment-aware failure trends, denominator-aware rates, benchmark-aware enrichment, and regression signals without changing the frozen failure schema. V5.8 adds end-to-end evidence tracing, exact per-run retrieval traces, retrieved-but-unused evidence detection, and document provenance inspection. V5.9 adds explicit versioned experiment configuration, canonical reproducibility hashes, and write-once configuration snapshots. V5.10 adds experiment discovery, selection, metric exploration, and comparison workflow improvements over the existing evaluation APIs.

See docs/methodology/v5.1-calibration.md, docs/methodology/v5.1-annotation-rubric.md, docs/methodology/v5.1-audit.md, docs/methodology/v5.2-benchmark.md, and docs/methodology/v5.2-audit.md, and docs/methodology/v5.3-retrieval-research.md, docs/methodology/v5.8-evidence-explorer.md, docs/methodology/v5.8-audit.md, docs/methodology/v5.9-reproducibility.md, and docs/methodology/v5.9-audit.md, and docs/methodology/v5.10-platform-ux.md, docs/methodology/v5.10-audit.md, docs/methodology/v5.11-research-reports.md, and docs/methodology/v5.11-audit.md.

## Important limitations

- ClinicalQA-v1 has 40 questions and remains a compact benchmark.
- Controlled corpus is compact.
- Lexical metrics remain as deterministic baselines alongside semantic evaluation.
- Human calibration labels are not yet populated.
- V4 uses a compact depression benchmark and has no hosted cloud deployment yet.
- No real patient data or autonomous clinical decision-making.
- The PostgreSQL runtime now uses Ollama semantic embeddings; the deterministic 256-dimensional provider remains available as a compatibility baseline.
- No clinical validation is claimed.

## Documentation

- docs/product-spec.md — product definition
- docs/roadmap.md — roadmap and phase status
- docs/data-model.md — core data model
- docs/failure-taxonomy.md — failure taxonomy
- docs/architecture/ — architecture and contracts
- docs/methodology/ — implementation methodology and audits
- docs/methodology/v2-audit.md — V2 freeze record
- docs/methodology/v3-audit.md — V3 freeze record
- docs/methodology/v4.10-audit.md — V4 productionization freeze record
- docs/methodology/v4.11-semantic-embeddings.md — semantic embedding hardening
- docs/methodology/v4.12-semantic-evaluation.md — semantic evaluation hardening
- docs/methodology/v4.15-failure-classifier.md — failure classifier hardening
- docs/methodology/v5.1-calibration.md — evaluator calibration
- docs/methodology/v5.1-annotation-rubric.md — human review rubric
- docs/methodology/v5.1-audit.md — V5.1 freeze record
- docs/roadmap-v5.md — V5 evaluation platform roadmap

## Tech direction

Python · FastAPI · PostgreSQL · pgvector · LLM provider abstraction · Docker · GitHub Actions · Ruff · mypy

Production infrastructure is introduced in later phases. V2 remains deliberately local and deterministic.

## License

Project license and contribution guidance will be added before public release.
