# V4 Roadmap — Productionization

V4.0–V4.10 are complete and frozen. The repository then entered a bounded **V4 Hardening** phase to address known methodological limitations without redefining V1–V3 domain contracts.

## V4.0–V4.10 — COMPLETE AND FROZEN
Production API, persistence, pgvector retrieval, provider integration, evaluation/failure runtime, observability, frontend, containers, CI/CD, and final audit.

## V4 Hardening

### V4.11 — Semantic Embeddings — COMPLETE AND FROZEN
- Ollama `nomic-embed-text` production embedding provider
- dedicated semantic pgvector column
- semantic HNSW index
- controlled-corpus re-indexing path
- deterministic hashed baseline retained

### V4.12 — Semantic Answer & Grounding Evaluation — NEXT
- model-assisted semantic evaluation behind provider boundaries
- deterministic lexical metrics retained as baselines
- evaluator version/configuration recorded
- calibration and regression coverage

### V4.13 — Benchmark Expansion — PLANNED
### V4.14 — Retrieval & Evaluation Challenge Set — PLANNED
### V4.15 — Failure Classifier Upgrade & Hardening Freeze — PLANNED

## Explicit exclusions

The hardening phase does not add FHIR, real patient data, autonomous clinical decisions, additional clinical domains, fine-tuning, multi-agent architecture, Kubernetes, or complex authentication.

V5 remains a separate future phase.
