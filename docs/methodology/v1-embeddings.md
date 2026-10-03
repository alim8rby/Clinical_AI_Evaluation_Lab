# V1.3 — Embeddings & Vector Storage

## Scope

V1.3 establishes the embedding and vector-storage boundary required by retrieval.

It provides a deterministic local baseline embedding and a JSON-backed development index. This is infrastructure only; it does not perform query retrieval or ranking.

## Contract

embed_text(text, dimensions) returns a normalized vector.

VectorIndex accepts Chunk records, stores vectors with complete chunk provenance, and can persist/reload the index.

## Limitation

The baseline embedding is a deterministic hashed-token representation. It is a development implementation, not a clinical semantic embedding model and must not be presented as retrieval-quality evidence.

A production embedding provider can replace embed_text behind this boundary.

## Excluded

Semantic search, ranking, reranking, external embedding APIs, pgvector, database persistence, and generation belong to later increments.
