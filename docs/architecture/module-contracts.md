# Module Contracts

## Purpose

V0.3 defines the boundaries between CAIEL modules. These contracts specify what each module receives, what it returns, and what it must not own.

Implementation details are deferred to later phases.

## Contract principles

1. Modules communicate through explicit data structures.
2. A module owns its transformation, not downstream behavior.
3. Provider-specific SDK types must not leak across module boundaries.
4. Evidence provenance must survive every transformation.
5. Failures must be represented explicitly rather than silently discarded.
6. Contracts should be stable enough to support unit and integration testing.

## 1. Ingestion

**Responsibility:** Convert an authoritative source into normalized Document records.

**Input**
- Source location or source content.
- Source metadata when available.

**Output**
- `Document`
- Parsed source content ready for preprocessing.

**Must not own**
- Retrieval
- Embedding generation
- Answer generation
- Evaluation

## 2. Preprocessing

**Responsibility:** Convert document content into clean, retrievable Chunks while preserving provenance.

**Input**
- `Document`
- Parsed document content

**Output**
- `Chunk[]`

**Required provenance**
- `document_id`
- `section`, when available
- `page`, when available
- `chunk_index`

**Must not own**
- Retrieval ranking
- LLM generation
- Evaluation

## 3. Retrieval

**Responsibility:** Find and rank evidence relevant to a clinical question.

**Input**
- Clinical question
- Retrieval configuration
- Available `Chunk` records

**Output**
- Ordered evidence set containing retrieved `Chunk` records and retrieval metadata.

**Required guarantee**
- Every returned chunk remains traceable to its source `Document`.

**Must not own**
- Answer wording
- Clinical interpretation
- Final evaluation

## 4. Generation

**Responsibility:** Produce a structured answer grounded in the supplied evidence.

**Input**
- Clinical question
- Ordered evidence set
- Generation/model configuration
- Prompt version

**Output**
- Structured `Answer`
  - answer text
  - claims
  - citations
  - uncertainty

**Required guarantee**
- Citations reference evidence available in the supplied evidence set.
- Provider-specific response objects are converted to CAIEL structures at this boundary.

**Must not own**
- Retrieval
- Persistent experiment tracking
- Final evaluation

## 5. Evaluation

**Responsibility:** Measure answer quality, grounding, reliability, and operational metrics.

**Input**
- `BenchmarkQuestion`
- `Answer`
- Retrieved evidence
- Evaluation configuration

**Output**
- `Evaluation[]`
- Optional `Failure[]` classifications when a defined failure is detected.

**Must not own**
- Generating or rewriting the answer
- Changing the source evidence
- Changing the benchmark question

## 6. Experiments

**Responsibility:** Orchestrate reproducible executions of a configured system.

**Input**
- `Experiment`
- `BenchmarkQuestion`
- Module configurations

**Output**
- `Run`
- Associated `Answer`
- Evaluation results

**Must not own**
- Provider-specific retrieval or generation logic
- Metric implementation details

## 7. Failure Analysis

**Responsibility:** Classify and expose reliability failures using the controlled failure taxonomy.

**Input**
- `Answer`
- `Evaluation`
- Supporting evidence
- Failure taxonomy

**Output**
- `Failure[]`

**Must not own**
- Answer generation
- Evidence retrieval
- Benchmark definition

## 8. Monitoring

**Responsibility:** Capture operational signals required to understand system behavior.

**Input**
- Run lifecycle events
- Latency
- Token usage
- Cost
- Errors

**Output**
- Operational records/metrics associated with the relevant `Run`.

**Must not own**
- Clinical evaluation scores
- Answer content transformation

## Cross-module data flow

```text
Document
   ↓
Ingestion
   ↓
Preprocessing
   ↓
Chunk[]
   ↓
Retrieval
   ↓
Evidence Set
   ↓
Generation
   ↓
Answer
   ├──→ Evaluation
   ├──→ Failure Analysis
   └──→ Monitoring
```

## Contract boundaries

| Boundary | Stable interface | Implementation deferred |
|---|---|---|
| Ingestion → Preprocessing | Document/content | Parser/library |
| Preprocessing → Retrieval | Chunk[] | Chunking algorithm/index |
| Retrieval → Generation | Evidence Set | Search/reranking implementation |
| Generation → Evaluation | Answer | LLM/provider |
| Evaluation → Failure Analysis | Evaluation + evidence | Evaluation algorithms |
| Experiments → Modules | Configuration + domain objects | Orchestration implementation |
| Modules → Monitoring | Run events/metrics | Telemetry backend |

## V0.3 scope boundary

V0.3 does not define:
- Python classes
- Pydantic schemas
- API routes
- database tables
- provider SDK implementations
- concrete embedding models
- concrete retrieval algorithms
