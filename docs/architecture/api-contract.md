# API Contract

## Purpose

V0.4 defines the external API surface for the CAIEL application. It describes routes, request intent, response shape, and error behavior without implementing the API.

## API principles

1. The API exposes product capabilities, not internal implementation details.
2. Responses preserve answer-to-evidence traceability.
3. Configuration is explicit for reproducible experiments.
4. Errors use a consistent structure.
5. V0 defines contracts only; FastAPI implementation is deferred.

## Base

```text
/api/v1
```

## 1. Health

### GET /health

Returns service availability.

**Response**
```json
{
  "status": "ok",
  "version": "string"
}
```

## 2. Clinical QA

### POST /qa

Submit a clinical question to the configured QA pipeline.

**Request**
```json
{
  "question": "string",
  "configuration": {
    "model": "string",
    "retriever": "string",
    "top_k": 5,
    "prompt_version": "string"
  }
}
```

**Response**
```json
{
  "run_id": "string",
  "answer": {
    "answer_id": "string",
    "answer_text": "string",
    "claims": [],
    "uncertainty": {}
  },
  "citations": [],
  "evidence": [],
  "metrics": {
    "latency_ms": 0,
    "input_tokens": 0,
    "output_tokens": 0,
    "cost": 0
  }
}
```

Each citation must identify the supported claim and the evidence chunk used.

## 3. Evidence Explorer

### GET /runs/{run_id}/evidence

Return the evidence retrieved for a run.

**Response**
```json
{
  "run_id": "string",
  "evidence": [
    {
      "chunk_id": "string",
      "document_id": "string",
      "text": "string",
      "section": "string",
      "page": 0,
      "rank": 1
    }
  ]
}
```

### GET /runs/{run_id}

Return the complete persisted result for a run.

**Response**
Includes:
- Run metadata
- Benchmark question
- Answer
- Citations
- Evidence
- Evaluation results, when available
- Failures, when available

## 4. Evaluation Lab

### POST /experiments

Create an experiment configuration.

**Request**
```json
{
  "name": "string",
  "description": "string",
  "model_config": {},
  "retriever_config": {},
  "prompt_version": "string",
  "benchmark_version": "string"
}
```

**Response**
Returns the created `Experiment` identifier and configuration.

### POST /experiments/{experiment_id}/runs

Run a benchmark question or benchmark set under an experiment.

**Request**
```json
{
  "question_ids": ["string"]
}
```

**Response**
```json
{
  "experiment_id": "string",
  "run_ids": ["string"],
  "status": "completed"
}
```

### GET /experiments/{experiment_id}

Return experiment configuration and execution summary.

## 5. Experiment Comparison

### POST /comparisons

Compare completed experiments using the same benchmark version.

**Request**
```json
{
  "experiment_ids": ["string"],
  "benchmark_version": "string"
}
```

**Response**
```json
{
  "benchmark_version": "string",
  "experiments": [],
  "metrics": {},
  "differences": []
}
```

The API returns measurements and differences without imposing a ranking or conclusion.

## 6. Failure Observatory

### GET /failures

List recorded failures.

**Query parameters**
- `category`
- `type`
- `experiment_id`
- `run_id`

**Response**
```json
{
  "failures": []
}
```

### GET /failures/{failure_id}

Return one failure with its supporting answer, evaluation, evidence, and taxonomy classification.

## Common error contract

All unsuccessful requests use:

```json
{
  "error": {
    "code": "string",
    "message": "string",
    "details": {}
  }
}
```

Initial error codes:

| Code | Meaning |
|---|---|
| `INVALID_REQUEST` | Request validation failed |
| `NOT_FOUND` | Requested resource does not exist |
| `RETRIEVAL_ERROR` | Evidence retrieval failed |
| `GENERATION_ERROR` | Answer generation failed |
| `EVALUATION_ERROR` | Evaluation failed |
| `SYSTEM_ERROR` | Unexpected internal failure |

## Contract rules

- IDs are opaque strings to API consumers.
- API consumers must not depend on database IDs or provider SDK objects.
- `run_id` is the primary trace identifier for a QA execution.
- Evidence returned by the API must retain document and chunk provenance.
- Evaluation and failure data are optional on a run until those stages complete.
- Batch experiment execution must preserve individual question/run traceability.

## V0.4 scope boundary

V0.4 does not implement:
- FastAPI routes
- Authentication
- Database persistence
- Streaming responses
- WebSockets
- Rate limiting
- Provider-specific API endpoints
