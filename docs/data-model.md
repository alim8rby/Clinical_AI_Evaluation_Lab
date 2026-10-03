# Core Data Model

## Purpose

This document defines the conceptual data model for CAIEL V0. It establishes the entities, fields, relationships, and traceability rules required by the evaluation laboratory.

V0 defines the model only. Database schemas, ORM models, migrations, and storage-specific implementation are deferred to later phases.

## Core entities

### Document
An authoritative source ingested into the controlled knowledge base.

| Field | Description |
|---|---|
| `document_id` | Stable unique identifier |
| `title` | Document title |
| `source` | Source or publisher |
| `organization` | Responsible organization |
| `publication_date` | Publication or release date |
| `url` | Canonical source URL |

### Chunk
A retrievable section of a document.

| Field | Description |
|---|---|
| `chunk_id` | Stable unique identifier |
| `document_id` | Parent document |
| `text` | Chunk content |
| `section` | Source section, when available |
| `page` | Source page, when available |
| `chunk_index` | Position within the document |

Chunk provenance remains linked to its parent document.

### BenchmarkQuestion
A reproducible clinical question used for evaluation.

| Field | Description |
|---|---|
| `question_id` | Stable unique identifier |
| `question` | Clinical question |
| `domain` | Clinical domain |
| `difficulty` | Benchmark difficulty |
| `expected_evidence` | Evidence expected to support the answer |
| `reference_answer` | Reference answer |
| `key_concepts` | Concepts expected in a correct answer |

### Experiment
A reproducible evaluation configuration.

| Field | Description |
|---|---|
| `experiment_id` | Stable unique identifier |
| `name` | Human-readable experiment name |
| `description` | Purpose of the experiment |
| `model_config` | Model/provider configuration snapshot |
| `retriever_config` | Retrieval configuration snapshot |
| `prompt_version` | Prompt version used |
| `benchmark_version` | Benchmark version used |
| `created_at` | Creation timestamp |

The configuration is stored with the experiment so runs can be reproduced and compared.

### Run
One execution of one benchmark question under an experiment.

| Field | Description |
|---|---|
| `run_id` | Stable unique identifier |
| `experiment_id` | Parent experiment |
| `question_id` | Benchmark question evaluated |
| `status` | Run status |
| `started_at` | Start timestamp |
| `finished_at` | Completion timestamp |
| `latency_ms` | End-to-end latency |
| `input_tokens` | Input token usage, when available |
| `output_tokens` | Output token usage, when available |
| `cost` | Estimated execution cost, when available |
| `error` | Error information, when applicable |

### Answer
The structured output produced by a run.

| Field | Description |
|---|---|
| `answer_id` | Stable unique identifier |
| `run_id` | Parent run |
| `answer_text` | Generated answer |
| `claims` | Structured claims extracted from the answer |
| `uncertainty` | Structured uncertainty information |

Claims are structured data inside an Answer rather than a separate top-level entity in V0.

### Citation
A traceable link from an answer claim to retrieved evidence.

| Field | Description |
|---|---|
| `citation_id` | Stable unique identifier |
| `answer_id` | Parent answer |
| `claim_index` | Claim within the answer being supported |
| `chunk_id` | Retrieved evidence chunk |
| `citation_text` | Citation/reference representation |

A citation resolves to a stored chunk and therefore to its source document.

### Evaluation
An evaluation result attached to an answer.

| Field | Description |
|---|---|
| `evaluation_id` | Stable unique identifier |
| `answer_id` | Evaluated answer |
| `evaluator_version` | Evaluation method/version |
| `scores` | Metric results |
| `details` | Supporting evaluation details |

An answer may have multiple evaluations when different evaluation methods are applied.

### Failure
A recorded reliability or system failure associated with an answer.

| Field | Description |
|---|---|
| `failure_id` | Stable unique identifier |
| `answer_id` | Associated answer |
| `category` | Failure category |
| `type` | Failure subtype |
| `description` | Failure description |
| `evidence` | Supporting evidence for the classification |

Allowed category/type values are defined by the failure taxonomy.

## Relationships

```text
Document 1 ─── N Chunk

Experiment 1 ─── N Run
BenchmarkQuestion 1 ─── N Run
Run 1 ─── 1 Answer

Answer 1 ─── N Citation
Answer 1 ─── N Evaluation
Answer 1 ─── N Failure

Citation N ─── 1 Chunk ─── 1 Document
```

## Traceability chain

```text
BenchmarkQuestion
      ↓
     Run
      ↓
    Answer
      ↓
   Claim
      ↓
   Citation
      ↓
    Chunk
      ↓
   Document
```

This enables the system to answer: **What did the model say, which claim was made, what evidence was cited, and which source document contains that evidence?**

## Reproducibility rules

1. Every persisted entity has a stable identifier.
2. Every Run records the Experiment and BenchmarkQuestion that produced it.
3. Every Experiment captures the configuration needed to reproduce its runs.
4. Every Citation resolves to a stored Chunk.
5. Every Chunk resolves to its source Document.
6. Evaluation results record the method/version used.
7. Failure records use the controlled failure taxonomy.
8. V0 does not prescribe a database, ORM, vector store, or serialization format.

## Deferred implementation

- SQL schema and migrations
- PostgreSQL/pgvector implementation
- ORM models
- API request/response schemas
- Pydantic models
- Embedding storage representation
- Physical indexes
- Database performance optimization
