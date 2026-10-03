# Clinical AI Evaluation Lab

**CAIEL** — an evidence-grounded framework for evaluating the reliability, retrieval quality, grounding, performance, and failure modes of LLM-based clinical question-answering systems.

> Portfolio engineering/research project. Not for patient care.

## Product

CAIEL is designed as an **evaluation laboratory**, not simply a medical chatbot.

The system will provide a controlled environment where an AI/ML engineer can:

1. Choose a system configuration
2. Ask a clinical question
3. Retrieve supporting evidence
4. Generate a structured answer
5. Inspect claims and citations
6. Evaluate reliability and performance
7. Inspect failures
8. Compare experiments

### Initial clinical domain

**Depression**

The V1 knowledge base and benchmark are intentionally limited to a controlled depression-focused corpus to keep evaluation reproducible.

### Primary user

AI/ML engineers working on healthcare AI.

Secondary users include healthcare AI researchers and clinical/domain experts.

---

## What has been built

### V0 — Architecture — FROZEN

The complete architectural foundation has been defined and audited before implementation begins.

#### V0.1 — Repository Architecture

Established the project structure and boundaries for:

- Application frontend/backend
- Ingestion
- Preprocessing
- Retrieval
- Generation
- Evaluation
- Experiment orchestration
- Failure analysis
- Monitoring
- Data
- Tests
- Configuration
- Documentation
- Scripts and notebooks

#### V0.2 — Core Data Model

Defined the conceptual entities and relationships:

- `Document`
- `Chunk`
- `BenchmarkQuestion`
- `Experiment`
- `Run`
- `Answer`
- `Citation`
- `Evaluation`
- `Failure`

The model preserves the complete evidence traceability chain:

```text
Benchmark Question
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

#### V0.3 — Module Contracts

Defined explicit boundaries for:

- Ingestion
- Preprocessing
- Retrieval
- Generation
- Evaluation
- Experiment orchestration
- Failure analysis
- Monitoring

Provider-specific implementations are kept behind stable module boundaries.

#### V0.4 — API Contract

Defined the initial application API surface:

- `GET /api/v1/health`
- `POST /api/v1/qa`
- `GET /api/v1/runs/{run_id}`
- `GET /api/v1/runs/{run_id}/evidence`
- `POST /api/v1/experiments`
- `POST /api/v1/experiments/{experiment_id}/runs`
- `GET /api/v1/experiments/{experiment_id}`
- `POST /api/v1/comparisons`
- `GET /api/v1/failures`
- `GET /api/v1/failures/{failure_id}`

A consistent API error contract and run-level traceability were also defined.

#### V0.5 — Configuration & Environment

Defined:

- Environment-variable contract
- Secret handling rules
- Non-secret configuration boundaries
- Provider/model abstraction
- Configuration precedence
- Experiment configuration snapshots
- Reproducibility rules
- Local development configuration expectations

No credentials are committed to the repository.

#### V0.6 — V0 Audit & Freeze

Audited the product specification, repository structure, data model, module contracts, API contract, configuration, and V1 boundary.

**Result: V0 FROZEN.**

Changes to V0 architecture should now happen only if V1 implementation exposes a concrete contract problem.

---

## Current architecture

### Runtime flow

```text
User
 ↓
Query Processor
 ↓
Retriever
 ├── Dense Search
 ├── BM25
 └── Reranker
 ↓
Evidence Set
 ↓
LLM
 ↓
Structured Answer
 ├── Claims
 ├── Citations
 └── Uncertainty
 ↓
Evaluation
 ↓
Storage
```

### Knowledge pipeline

```text
Authoritative Documents
 ↓
Ingestion
 ↓
Parsing
 ↓
Cleaning
 ↓
Chunking
 ↓
Metadata
 ↓
Embeddings
 ↓
Vector Storage
 ↓
Retrieval
```

### Core architectural principle

Every generated answer must remain traceable to:

**Answer → Claim → Citation → Chunk → Document**

This traceability is fundamental to the evaluation and failure-analysis capabilities of CAIEL.

---

## Evaluation framework

CAIEL is designed to evaluate five dimensions.

### Retrieval

- Precision@K
- Recall@K
- MRR
- nDCG

### Generation

- Correctness
- Completeness
- Relevance

### Grounding

- Faithfulness
- Citation correctness
- Unsupported claim rate

### Reliability

- Hallucination rate
- Critical error rate
- Uncertainty handling
- Unsupported recommendation rate

### Operations

- Latency
- Token usage
- Cost
- Failure rate

---

## Failure taxonomy

CAIEL uses a controlled failure taxonomy:

### Retrieval
- Missing evidence
- Wrong document
- Wrong chunk
- Ranking failure

### Generation
- Hallucination
- Incorrect interpretation
- Incomplete answer
- Unsupported claim

### Citation
- Wrong citation
- Citation does not support claim

### Safety
- Overconfidence
- Missing uncertainty
- Potentially unsafe output

### System
- API failure
- Timeout
- Invalid output

---

## Repository structure

```text
clinical-ai-evaluation-lab/
│
├── app/
│   ├── frontend/
│   └── backend/
│
├── src/
│   ├── ingestion/
│   ├── preprocessing/
│   ├── retrieval/
│   ├── generation/
│   ├── evaluation/
│   ├── experiments/
│   ├── failure_analysis/
│   └── monitoring/
│
├── data/
│   ├── raw/
│   ├── processed/
│   ├── benchmark/
│   └── results/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── retrieval/
│   └── evaluation/
│
├── configs/
├── notebooks/
├── scripts/
│
├── docs/
│   ├── architecture/
│   ├── methodology/
│   ├── experiments/
│   └── safety/
│
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
└── docker-compose.yml
```

---

## Documentation

The V0 architecture is documented in:

- `docs/product-spec.md` — frozen product specification
- `docs/roadmap.md` — development roadmap
- `docs/data-model.md` — core conceptual data model
- `docs/failure-taxonomy.md` — controlled failure taxonomy
- `docs/architecture/system.md` — system architecture
- `docs/architecture/repository.md` — repository boundaries
- `docs/architecture/decisions.md` — architecture decisions
- `docs/architecture/module-contracts.md` — module interfaces
- `docs/architecture/api-contract.md` — API surface
- `docs/architecture/configuration.md` — configuration and environment contract
- `docs/architecture/v0-audit.md` — V0 audit and freeze record

---

## What is intentionally not built yet

V0 is architecture-only. The repository does **not** yet claim to have:

- A working RAG pipeline
- Document ingestion implementation
- Embedding generation
- Vector database
- Retrieval implementation
- LLM generation implementation
- Automated evaluation pipeline
- Experiment execution engine
- Failure analysis engine
- Production database
- Frontend application
- Deployed service
- CI/CD pipeline

These are implementation stages of V1 and later.

---

## Roadmap

| Phase | Status | Scope |
|---|---|---|
| **V0 — Architecture** | **FROZEN** | Product boundary, repository architecture, data model, module contracts, API contract, configuration, audit |
| **V1 — Working RAG** | Next | Ingestion, preprocessing, embeddings, retrieval, generation, citations |
| **V2 — Evaluation Lab** | Planned | ClinicalQA-v1 benchmark, automated evaluation, experiment tracking, comparisons |
| **V3 — Failure Observatory** | Planned | Failure classification, analysis UI, regression testing |
| **V4 — Productionization** | Planned | API implementation, database, logging, monitoring, Docker, deployment, CI/CD |
| **V5 — Healthcare interoperability** | Planned | FHIR, provenance, structured clinical data, human-in-the-loop workflows |

---

## Scope exclusions

The initial release explicitly excludes:

- General medical knowledge
- Real patient data
- Autonomous clinical decisions
- EHR integration
- Mobile application
- Voice interface
- Fine-tuning
- Multi-agent architecture
- FHIR implementation in V1
- Kubernetes
- Complex authentication
- Multiple medical domains

---

## Technology direction

The planned implementation stack is:

- Python
- FastAPI
- PostgreSQL
- pgvector
- LLM provider abstraction
- Modern lightweight web UI
- Docker
- Git/GitHub
- pytest

Specific providers, models, embedding implementations, frontend framework, and deployment platform remain implementation decisions for later phases.

## Project status

**Current phase: V0 complete and frozen.**

**Next implementation phase: V1 — Working RAG.**
