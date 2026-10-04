# Roadmap

## V0 — Architecture — FROZEN

Completed: repository architecture, core data model, module contracts, API contract, configuration, audit and freeze.

## V1 — Working RAG — FROZEN

Completed: ingestion, preprocessing, embeddings/vector index, retrieval, generation boundary, citations, end-to-end RAG, integration/failure-path tests, audit and freeze.

## V2 — Evaluation Lab — FROZEN

Completed:
1. Evaluation architecture
2. ClinicalQA-v1 benchmark and controlled evidence corpus
3. Retrieval evaluation
4. Answer evaluation
5. Grounding and citation evaluation
6. Reliability evaluation
7. Experiment tracking
8. Experiment comparison
9. Reproducible evaluation reports
10. V2 audit and freeze

V2 is a deterministic engineering evaluation baseline, not a clinically validated benchmark or safety classifier.

## V3 — Failure Observatory — FROZEN

Completed:
1. Failure architecture and scope
2. Failure data model and serialization
3. Deterministic classification
4. Severity and triage rules
5. Local structured persistence
6. Failure analysis and filtering
7. Regression suite for known failure conditions
8. Observatory query/backend boundary
9. Failure Observatory UI
10. End-to-end failure workflow integration
11. V3 audit and freeze

V3 remains local. It does not introduce PostgreSQL, production APIs, authentication, deployment infrastructure, or other V4 concerns.

V3 severity is a deterministic triage signal, not a validated clinical risk score. Failure classification is heuristic and engineering-oriented.

## V4 — Productionization — FROZEN

Completed: FastAPI implementation, PostgreSQL and pgvector, structured persistence, logging and monitoring, Docker deployment stack, CI/CD, and final audit/freeze.

## V5 — Healthcare interoperability — PLANNED

Planned:
- FHIR
- Provenance
- Structured clinical data
- Human-in-the-loop workflows
