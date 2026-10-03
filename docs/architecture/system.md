# System Architecture

## Purpose

CAIEL evaluates evidence-grounded clinical question-answering systems.

## Runtime flow

```
User
  ↓
Query Processor
  ↓
Retriever
  ├── Dense Search
  ├── BM25
  └── Reranker
  ↓
Evidence Set
  ↓
LLM
  ↓
Structured Answer
  ├── Claims
  ├── Citations
  └── Uncertainty
  ↓
Evaluation
  ↓
Storage
```

## Knowledge flow

```
Authoritative Documents
  ↓
Ingestion
  ↓
Parsing
  ↓
Cleaning
  ↓
Chunking
  ↓
Metadata
  ↓
Embeddings
  ↓
Vector Storage
  ↓
Retrieval
```

## Architectural principle

The system must preserve the relationship between an answer, its claims, its citations, and the evidence retrieved from the controlled knowledge base.

## Scope boundary

V0 defines the architecture only. Implementations of retrieval, generation, evaluation, and persistence begin in later phases.
