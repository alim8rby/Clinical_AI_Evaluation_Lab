# V4.3 pgvector Retrieval

V4.3 adds a production retrieval boundary around the existing EvidenceSet contract.

- EmbeddingProvider isolates embedding implementations.
- LocalHashedEmbeddingProvider preserves the V1 deterministic baseline for development.
- PgVectorRetriever queries PostgreSQL/pgvector.
- Chunk provenance is preserved.
- PostgreSQL uses cosine distance with deterministic chunk_id tie-breaking.
- Migration 002 enables vector and an HNSW cosine index.

The current embedding remains the deterministic hashed-token baseline. V4.4 will add a real provider.