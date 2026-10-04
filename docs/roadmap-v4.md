# V4 Roadmap — Productionization

## Goal

Turn the frozen V1–V3 local system into a deployable application without changing the frozen domain contracts.

## Scope

V4 is infrastructure and application delivery. It does not redefine RAG semantics, evaluation metrics, failure taxonomy, failure severity rules, or benchmark semantics.

## V4.0 — Production API Foundation — COMPLETE AND FROZEN
- FastAPI application
- /api/v1 route boundary
- health endpoint
- structured error contract
- dependency/configuration boundary
- API tests

## V4.1 — API Domain Adapters — COMPLETE AND FROZEN
- QA endpoint
- experiment endpoints
- comparison endpoint
- run/evidence endpoints
- failure Observatory endpoints
- Pydantic request/response models
- domain-to-API mapping

## V4.2 — PostgreSQL Persistence — COMPLETE AND FROZEN
- SQLAlchemy persistence boundary
- database models for core entities
- migrations
- repository interfaces
- replace local JSON persistence where appropriate

## V4.3 — pgvector Retrieval — COMPLETE AND FROZEN
- production embedding provider boundary
- PostgreSQL/pgvector index
- document/chunk ingestion persistence
- retrieval repository
- preserve chunk provenance

## V4.4 — Real LLM Provider Integration — COMPLETE AND FROZEN
- provider abstraction implementation
- configurable model selection
- structured generation output
- timeout/error handling
- provider-neutral domain contracts

## V4.5 — Evaluation/Failure Runtime — COMPLETE AND FROZEN
- execute benchmark runs through the application
- persist evaluation results
- persist failures
- experiment execution
- comparison/report access

## V4.6 — Observability — COMPLETE AND FROZEN
- structured logging
- request/run correlation IDs
- latency/token/cost tracking
- application metrics
- failure logging
- health/readiness checks

## V4.7 — Frontend Integration — COMPLETE AND FROZEN
- replace V3 demo fixture with API data
- connect QA workflow
- connect Observatory
- experiment and comparison views
- evidence/traceability views

## V4.8 — Containerization & Local Deployment — COMPLETE AND FROZEN
- Dockerfile
- production compose setup
- environment configuration
- database initialization
- health checks

## V4.9 — CI/CD & Deployment — COMPLETE AND FROZEN
- automated test pipeline
- lint/type checks
- image build
- deployment configuration
- production secrets boundary

## V4.10 — V4 Audit & Freeze — COMPLETE AND FROZEN
- API contract audit
- persistence audit
- retrieval audit
- provider audit
- observability audit
- security/configuration audit
- deployment audit
- V1–V3 compatibility audit
- documentation
- freeze

## Explicit exclusions

V4 does not include FHIR, real patient data, autonomous clinical decisions, additional clinical domains, fine-tuning, multi-agent architecture, Kubernetes unless later justified, or complex authentication before the application requires it.

## Definition of done

V4 is complete when the frozen CAIEL domain can run behind a real API, persist its core data in PostgreSQL, perform production-style retrieval and generation through provider boundaries, expose evaluation/failure workflows, serve the UI from real data, emit operational telemetry, and run reproducibly through containers and CI/CD.
