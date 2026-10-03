# Architecture Decisions

## ADR-001 — Evaluation laboratory rather than chatbot

CAIEL is designed around measurement, traceability, and failure analysis. Clinical question answering is the system under evaluation, not the product goal by itself.

## ADR-002 — Controlled domain for V1

V1 uses depression as the initial clinical domain. This keeps the knowledge base and benchmark bounded enough for reproducible evaluation.

## ADR-003 — Provider abstraction

The generation layer should not depend directly on one model provider. Provider-specific integrations belong behind a stable application interface.

## ADR-004 — Evidence traceability

Retrieved evidence must retain provenance metadata so claims can be traced back to source material.

## Deferred decisions

Specific LLM provider, embedding model, vector-store implementation details, frontend framework, deployment platform, and production infrastructure are deliberately deferred until their implementation phase requires them.
