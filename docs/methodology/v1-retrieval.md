# V1.4 — Retrieval

## Scope

V1.4 converts a clinical question into a ranked evidence set from the V1.3 vector index.

## Contract

retrieve(index, query, top_k) returns an EvidenceSet.

Each Evidence record contains:

- the original Chunk;
- a similarity score;
- a one-based rank.

Every result therefore remains traceable through:

Evidence → Chunk → Document.

## Ranking

The current development implementation uses cosine similarity between the deterministic local query embedding and stored chunk vectors. Ties are resolved by chunk_id for deterministic ordering.

## Excluded

V1.4 does not implement:

- LLM generation;
- reranking;
- BM25 or hybrid retrieval;
- external embedding providers;
- database-backed vector search;
- evaluation metrics.

## Limitation

Because V1.3 uses a deterministic hashed-token baseline embedding, retrieval quality is a development baseline rather than a clinical retrieval-quality result. A production embedding implementation can replace the embedding provider without changing the EvidenceSet contract.
