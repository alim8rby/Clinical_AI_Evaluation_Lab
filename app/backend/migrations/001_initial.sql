CREATE TABLE documents (
    document_id VARCHAR(64) PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    source VARCHAR(500) NOT NULL,
    organization VARCHAR(500) NOT NULL,
    publication_date DATE,
    url VARCHAR(2000) NOT NULL,
    content TEXT NOT NULL
);

CREATE TABLE chunks (
    chunk_id VARCHAR(64) PRIMARY KEY,
    document_id VARCHAR(64) NOT NULL,
    text TEXT NOT NULL,
    section VARCHAR(500),
    page INTEGER,
    chunk_index INTEGER NOT NULL
);

CREATE TABLE experiments (
    experiment_id VARCHAR(64) PRIMARY KEY,
    name VARCHAR(500) NOT NULL,
    description TEXT NOT NULL,
    model_config JSON NOT NULL,
    embedding_config JSON NOT NULL,
    retriever_config JSON NOT NULL,
    top_k INTEGER NOT NULL,
    prompt_version VARCHAR(100) NOT NULL,
    benchmark_version VARCHAR(100) NOT NULL,
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE runs (
    run_id VARCHAR(64) PRIMARY KEY,
    experiment_id VARCHAR(64) NOT NULL,
    question_id VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL,
    started_at TIMESTAMP NOT NULL,
    finished_at TIMESTAMP,
    latency_ms FLOAT,
    input_tokens INTEGER,
    output_tokens INTEGER,
    cost FLOAT,
    error TEXT
);

CREATE TABLE answers (
    answer_id VARCHAR(100) PRIMARY KEY,
    run_id VARCHAR(64) NOT NULL,
    answer_text TEXT NOT NULL,
    claims JSON NOT NULL,
    uncertainty TEXT,
    model VARCHAR(200) NOT NULL,
    prompt_version VARCHAR(100) NOT NULL
);

CREATE TABLE citations (
    citation_id VARCHAR(150) PRIMARY KEY,
    answer_id VARCHAR(100) NOT NULL,
    claim_index INTEGER NOT NULL,
    chunk_id VARCHAR(64) NOT NULL,
    citation_text TEXT NOT NULL
);

CREATE TABLE evaluations (
    evaluation_id VARCHAR(100) PRIMARY KEY,
    answer_id VARCHAR(100) NOT NULL,
    evaluator_version VARCHAR(100) NOT NULL,
    scores JSON NOT NULL,
    details JSON NOT NULL
);

CREATE TABLE failures (
    failure_id VARCHAR(150) PRIMARY KEY,
    run_id VARCHAR(64) NOT NULL,
    question_id VARCHAR(100) NOT NULL,
    answer_id VARCHAR(100),
    category VARCHAR(100) NOT NULL,
    type VARCHAR(200) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    description TEXT NOT NULL,
    evidence TEXT NOT NULL,
    metric VARCHAR(200),
    metric_value FLOAT,
    classifier_version VARCHAR(100) NOT NULL,
    created_at TIMESTAMP
);

CREATE INDEX idx_chunks_document ON chunks(document_id);
CREATE INDEX idx_runs_experiment ON runs(experiment_id);
CREATE INDEX idx_runs_question ON runs(question_id);
CREATE INDEX idx_answers_run ON answers(run_id);
CREATE INDEX idx_citations_answer ON citations(answer_id);
CREATE INDEX idx_evaluations_answer ON evaluations(answer_id);
CREATE INDEX idx_failures_run ON failures(run_id);
CREATE INDEX idx_failures_question ON failures(question_id);
CREATE INDEX idx_failures_category ON failures(category);
CREATE INDEX idx_failures_type ON failures(type);
CREATE INDEX idx_failures_severity ON failures(severity);
