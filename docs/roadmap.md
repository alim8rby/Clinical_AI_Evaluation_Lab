# Roadmap

## V0 — Architecture — FROZEN

Completed: repository architecture, core data model, module contracts, API contract, configuration, audit and freeze.

## V1 — Working RAG — FROZEN

Completed: ingestion, preprocessing, embeddings/vector index, retrieval, generation boundary, citations, end-to-end RAG, integration/failure-path tests, audit and freeze.

## V2 — Evaluation Lab — FROZEN

Completed: benchmark and controlled evidence corpus, retrieval evaluation, answer evaluation, grounding and citation evaluation, reliability evaluation, experiment tracking, comparison, reproducible reports, and audit/freeze.

V2 is a deterministic engineering evaluation baseline, not a clinically validated benchmark or safety classifier.

## V3 — Failure Observatory — FROZEN

Completed: failure architecture, data model, deterministic classification, severity and triage, persistence, analysis, regression suite, observatory backend/UI, and end-to-end workflow integration.

V3 severity is a deterministic triage signal, not a validated clinical risk score. Failure classification is heuristic and engineering-oriented.

## V4 — Productionization — FROZEN

Completed: FastAPI implementation, PostgreSQL and pgvector, structured persistence, semantic embeddings, semantic answer/grounding evaluation, expanded benchmark, retrieval challenge set, failure classifier v2, observability, frontend, containers, CI/CD, and final hardening audit.

## V5 — Evaluation Platform — IN PROGRESS

See `docs/roadmap-v5.md`.

Current phase: **V5.11 — Research Reports — NEXT**.

V5.10 platform UX is engineering complete and frozen. Empirical results remain execution-dependent.

V5.3–V5.7 evaluation-platform engineering phases are complete. Empirical results remain execution-dependent.

V5.1 engineering is frozen; human calibration labels remain optional and pending.
