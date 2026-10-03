# Module Contracts

## Purpose

V0.3 defines the boundaries between CAIEL modules. These contracts specify what each module receives, what it returns, and what it must not own.

## Contract principles

1. Modules communicate through explicit data structures.
2. A module owns its transformation, not downstream behavior.
3. Provider-specific SDK types must not leak across module boundaries.
4. Evidence provenance must survive every transformation.
5. Failures must be represented explicitly rather than silently discarded.
6. Contracts should be stable enough to support unit and integration testing.

## 1. Ingestion

**Responsibility:** Convert an authoritative source into a normalized `SourceDocument`.

**Input**
- Source content.
- Source metadata.

**Output**
- `SourceDocument` wrapped in an `IngestionResult`.

**Must not own**
- Retrieval
- Embedding generation
- Answer generation
- Evaluation

## 2. Preprocessing

**Responsibility:** Convert document content into clean, retrievable Chunks while preserving provenance.

**Input**
- `SourceDocument`

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
- Ordered `EvidenceSet` containing retrieved `Chunk` records and retrieval metadata.

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
  - evidence references
  - uncertainty
  - model identifier
  - prompt version

**Required guarantee**
- Claim evidence references point to evidence supplied to the provider.
- Provider-specific response objects are converted to CAIEL structures at this boundary.

**Must not own**
- Retrieval
- Persistent experiment tracking
- Final evaluation

## 5. Citation & Traceability

**Responsibility:** Turn claim evidence references into explicit, validated `Citation` records.

**Input**
- `Answer`
- `EvidenceSet`
- Answer identity

**Output**
- `Citation[]`

**Required guarantee**
- Every citation resolves to a chunk in the supplied evidence set.
- The resulting chain remains traceable from answer → claim → citation → chunk → document.

**Must not own**
- Claim generation
- Retrieval
- Evaluation of whether evidence semantically supports a claim

## 6. Evaluation

**Responsibility:** Measure answer quality, grounding, reliability, and operational metrics.

**Input**
- `BenchmarkQuestion`
- `Answer`
- Retrieved evidence
- Evaluation configuration

**Output**
- BCEvaluation[]`
- Optional `Failure[]` classifications when a defined failure is detected.

**Must not own**
- Generating or rewriting the answer
- Changing the source evidence
- Changing the benchmark question

## 7. Experiments

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

## 8. Failure Analysis

**Responsibility:** Classify and expose reliability failures using the controlled failure taxonomy.

**Input**
- `Answer`
- BCEvaluation`
- Supporting evidence
- Failure taxonomy

**Output**
- `Failure[]`

**Must not own**
- Answer generation
- Evidence retrieval
- Benchmark definition

## 9. Monitoring

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

``text
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
   ↓
Citation & Traceability
   ├──→ Evaluation
   ├──→ Failure Analysis
   └──→ Monitoring
``

## Contract boundaries

| Boundary | Stable interface | Implementation |
|---|---|---|
| Ingestion → Preprocessing | SourceDocument | Implemented in V1 |
| Preprocessing → Retrieval | Chunk[] | Implemented in V1 |
| Retrieval → Generation | EvidenceSet | Implemented in V1 |
| Generation → Citation | Answer + evidence references | Implemented in V1 |
| Citation → Evaluation | Citation[] | Evaluation deferred to V2 |
| Evaluation → Failure Analysis | Evaluation + evidence | Evaluation algorithms deferred |
| Experiments → Modules | Configuration + domain objects | Deferred |
| Modules → Monitoring | Run events/metrics | Deferred |

## V0.3 scope boundary

V0.3 does not define:
- Python implementation details
- Pydantic schemas
- API implementation
- database tables
- provider SDK implementations
- concrete embedding models
- concrete retrieval algorithms
