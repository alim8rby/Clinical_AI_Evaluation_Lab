CREATE EXTENSION IF NOT EXISTS vector;

ALTER TABLE chunks
    ADD COLUMN IF NOT EXISTS embedding vector(256);

CREATE INDEX IF NOT EXISTS idx_chunks_embedding
    ON chunks USING hnsw (embedding vector_cosine_ops);
