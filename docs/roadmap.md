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

## V3 — Failure Observatory — NEXT

Planned:
- Failure classification and persistence
- Failure analysis workflows
- Failure Observatory UI
- Regression testing around known failures

## V4 — Productionization — PLANNED

Planned:
- FastAPI implementation
- PostgreSQL and pgvector
- Structured persistence
- Logging and monitoring
- Docker and deployment
- CI/CD

## V5 — Healthcare interoperability — PLANNED

Planned:
- FHIR
- Provenance
- Structured clinical data
- Human-in-the-loop workflows
