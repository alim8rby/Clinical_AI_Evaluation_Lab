# Architecture Decisions

These decisions explain why CAIEL is structured as an evaluation platform rather than a conventional RAG chatbot.

## ADR-001 — Evaluation laboratory rather than chatbot

CAIEL is designed around measurement, traceability, and failure analysis. Clinical question answering is the system under evaluation, not the product goal by itself.

## ADR-002 — Controlled domain for V1

V1 uses depression as the initial clinical domain. This keeps the knowledge base and benchmark bounded enough for reproducible evaluation.

## ADR-003 — Provider abstraction

The generation layer should not depend directly on one model provider. Provider-specific integrations belong behind a stable application interface.

## ADR-004 — Evidence traceability

Retrieved evidence must retain provenance metadata so claims can be traced back to source material.

## ADR-005 — Evidence-first generation

Retrieval produces an explicit evidence set before generation.

**Why:** Retrieval quality must be measurable independently from generation quality, and downstream claims need an inspectable evidence boundary.

## ADR-006 — Structured answers

Answers contain claims, citations, and uncertainty.

**Why:** Plain text cannot support reliable claim-level inspection. Structured answers make grounding and citation evaluation possible.

## ADR-007 — Separate evaluation dimensions

Retrieval, answer quality, grounding, and reliability are evaluated separately.

**Why:** A single score hides failure modes. Separate dimensions make it possible to identify where a system failed.

## ADR-008 — Persisted failure records

Evaluation failures are persisted as structured records rather than represented only by aggregate metrics.

**Why:** Aggregate metrics show that something changed; failure records help explain what changed and where.

## ADR-009 — Immutable experiment configuration

Experiment configuration is write-once and receives a reproducibility hash.

**Why:** A result is difficult to interpret if the configuration that produced it can silently change afterward.

## ADR-010 — Portfolio/research boundary

The current system is explicitly outside clinical production. The benchmark is an engineering dataset, model-assisted evaluation is not clinical ground truth, and the V5 audit documents known production-security and deployment boundaries.

## Deferred decisions

Hosted deployment, production authentication/authorization, production ingress/TLS, secret management, and other production infrastructure remain outside the frozen V5 scope.
