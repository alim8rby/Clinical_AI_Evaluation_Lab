ALTER TABLE experiments
    ADD COLUMN IF NOT EXISTS reproducibility_snapshot JSON;

ALTER TABLE experiments
    ADD COLUMN IF NOT EXISTS reproducibility_hash VARCHAR(64);

CREATE INDEX IF NOT EXISTS idx_experiments_reproducibility_hash
    ON experiments(reproducibility_hash);
