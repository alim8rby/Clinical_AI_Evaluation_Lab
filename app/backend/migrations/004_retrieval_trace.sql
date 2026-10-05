CREATE TABLE IF NOT EXISTS retrieval_traces (
    retrieval_id VARCHAR(150) PRIMARY KEY,
    run_id VARCHAR(64) NOT NULL,
    chunk_id VARCHAR(64) NOT NULL,
    rank INTEGER NOT NULL,
    score FLOAT
);

CREATE INDEX IF NOT EXISTS idx_retrieval_traces_run ON retrieval_traces(run_id);
CREATE INDEX IF NOT EXISTS idx_retrieval_traces_chunk ON retrieval_traces(chunk_id);
