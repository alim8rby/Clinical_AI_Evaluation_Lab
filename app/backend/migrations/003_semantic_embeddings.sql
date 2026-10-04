ALTER TABLE chunks
    ADD COLUMN IF NOT EXISTS semantic_embedding vector(768);

CREATE INDEX IF NOT EXISTS idx_chunks_semantic_embedding
    ON chunks USING hnsw (semantic_embedding vector_cosine_ops);
