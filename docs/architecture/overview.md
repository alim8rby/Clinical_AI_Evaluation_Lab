# CAIEL Architecture Overview

CAIEL is organized around one principle:

> **An AI answer is only useful as an evaluation artifact when its evidence, claims, configuration, and evaluation signals remain inspectable.**

## Runtime architecture

```text
User Question
      │
      ▼
Query / Retrieval
      │
      ├── Dense retrieval
      ├── BM25 / hybrid research strategies
      └── Retrieval trace
      │
      ▼
Evidence Set
      │
      ▼
Generation Provider
      │
      ▼
Structured Answer
      │
      ├── Claims
      ├── Citations
      └── Uncertainty
      │
      ▼
Evaluation Layer
      │
      ├── Retrieval
      ├── Answer quality
      ├── Grounding
      └── Reliability
      │
      ▼
Failure Analysis
      │
      ▼
Experiment / Statistical Analysis
      │
      ▼
Research Report
```

## Knowledge flow

```text
Controlled source documents
      ↓
Ingestion
      ↓
Parsing / preprocessing
      ↓
Chunking + metadata
      ↓
Embeddings
      ↓
PostgreSQL + pgvector
      ↓
Retrieval
```

The current demonstration corpus is a compact depression-focused engineering dataset.

## Core boundaries

### Retrieval is separated from generation

The retriever produces an explicit evidence set. The generator consumes that evidence rather than accessing the knowledge store implicitly.

This makes retrieval quality independently measurable.

### Answers are structured

An answer is represented with claims, citations, and uncertainty rather than being stored as an opaque text string.

This enables claim-level grounding and evidence inspection.

### Evaluation is separate from execution

The runtime orchestrates evaluation modules; retrieval, answer, grounding, and reliability metrics remain independently defined.

This allows different evaluation strategies to be compared without changing the core RAG flow.

### Failures are first-class records

Evaluation signals can produce structured failure records with category, type, severity, metric, evidence, and classifier version.

The Failure Observatory derives experiment-level views from those records.

### Experiments are reproducible by configuration identity

An experiment records its model, embedding, retriever, prompt, benchmark, evaluator, runtime, and reproducibility hash.

Configuration is immutable once persisted.

### Evidence is traceable

A completed run can be inspected through:

```text
Question
  → Answer
  → Claim
  → Citation
  → Retrieved Chunk
  → Source Document
```

Retrieval traces also preserve evidence that was retrieved but not cited.

## Persistence architecture

The application uses:

- **FastAPI** for the API boundary
- **PostgreSQL + pgvector** for experiment/runtime persistence and vector retrieval
- **Repository adapters** for persistence access
- **Ollama** for local generation and embedding providers
- **Docker Compose** for the local multi-service environment

The domain/evaluation modules remain separated from HTTP and database concerns where practical.

## Production boundary

The current architecture is intentionally a portfolio/research deployment.

The V5 audit documents known non-production boundaries including authentication/authorization, rate limiting, TLS, secret management, production ingress, and hosted deployment.

CAIEL therefore demonstrates evaluation engineering and platform design; it does not claim production clinical deployment.

## Architectural invariants

1. Evidence must be explicit before generation.
2. Claims and citations must remain inspectable.
3. Evaluation signals must remain separate from clinical claims.
4. Experiment configuration must be immutable after creation.
5. Failure records must retain their original run/question linkage.
6. Research reports must expose methodology and limitations.
