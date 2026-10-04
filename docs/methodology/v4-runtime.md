# V4.5 — Evaluation and Failure Runtime

V4.5 connects the frozen V1–V3 domain to the V4 persistence layer.

## Runtime flow

Benchmark question → Experiment → Run → RAG → retrieval evaluation → answer evaluation → grounding → reliability → failure classification → PostgreSQL persistence.

The application runtime owns orchestration. Existing evaluation, experiment, and failure-analysis modules remain domain-owned.

## Persistence

A completed run stores run metadata, the generated answer and claims, citations, one evaluation record for each evaluation group, and classified failures. Failed runs retain their run record and error message.

## Provider boundary

The runtime consumes the existing ClinicalRAG provider boundary. V4.4 Ollama providers can be injected by the application without changing the evaluation contracts.

## Failure boundary

V3 classification is reused unchanged. V4 supplies a SQL adapter implementing the same persistence surface expected by the V3 workflow.

## Design constraint

FastAPI routes should call application services and adapters only. Evaluation and failure logic must not move into route handlers.
