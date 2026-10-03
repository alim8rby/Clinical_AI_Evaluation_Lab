# Clinical AI Evaluation Lab

**CAIEL** is a portfolio project for building and evaluating evidence-grounded clinical QA systems.

The goal is not just to make a medical chatbot. The goal is to make it possible to see **where an AI answer came from, how reliable it is, and where it fails**.

> Portfolio/research project. Not for patient care.

## Current status

**V1 — Working RAG: FROZEN**

The repository now contains a complete local RAG path:

```text
Source document
      ↓
Ingestion
      ↓
Chunking
      ↓
Embeddings + vector index
      ↓
Retrieval
      ↓
Generation
      ↓
Citations
```

The implementation is intentionally local and deterministic at this stage. It uses a simple hashed-token embedding and a mock generation provider, so V1 is an engineering baseline rather than a clinically validated system.

## What V1 includes

- Document ingestion and provenance
- Deterministic document and chunk IDs
- Document chunking
- Local JSON-backed vector index
- Ranked retrieval
- Generation provider interface
- Deterministic mock generator
- Claim-level evidence references
- Citation validation
- End-to-end RAG pipeline
- Unit tests
- Integration and failure-path tests

The main traceability chain is:

```text
Question → Evidence → Answer → Claim → Citation → Chunk → Document
```

## Example flow

A question enters the RAG pipeline, evidence is retrieved from the indexed documents, an answer is generated from that evidence, and the citation layer checks that every claim points to retrieved evidence.

This gives the project a clear base for the next step: measuring reliability rather than only generating answers.

## Evaluation plan

V2 will add the actual evaluation lab:

- ClinicalQA-v1 benchmark
- Retrieval metrics
- Answer quality metrics
- Grounding and citation evaluation
- Experiment tracking
- Model/retriever/prompt comparisons

Later phases will add failure analysis, API/database infrastructure, monitoring, and deployment.

## Known limitations

V1 is deliberately small.

- The embedding model is a deterministic hashed-token baseline.
- The generation provider is a local mock.
- The vector index is JSON-backed.
- No real clinical corpus is included yet.
- Citation validation checks references, not whether evidence truly supports a claim.
- No automated clinical evaluation exists yet.
- No API, database, frontend, or deployment exists yet.

These are planned work, not hidden capabilities.

## Project structure

```text
app/                  Application layer
src/
  ingestion/          Document ingestion
  preprocessing/      Chunking
  retrieval/          Embeddings and retrieval
  generation/         Answer generation and citations
  evaluation/         Future evaluation layer
  experiments/        Future experiment layer
  failure_analysis/   Future failure analysis
  monitoring/         Future monitoring

data/
  raw/
  processed/
  benchmark/
  results/

tests/
  unit/
  integration/
  retrieval/
  evaluation/

docs/
  architecture/
  methodology/
  experiments/
  safety/
```

## Documentation

Start with:

- `docs/product-spec.md` — product definition
- `docs/roadmap.md` — development roadmap
- `docs/data-model.md` — core data model
- `docs/failure-taxonomy.md` — failure taxonomy
- `docs/architecture/` — system and module contracts
- `docs/methodology/` — V1 implementation notes
- `docs/methodology/v1-audit.md` — V1 audit and freeze record

## Roadmap

| Phase | Status | Main goal |
|---|---|---|
| V0 | FROZEN | Architecture and contracts |
| V1 | FROZEN | Working local RAG |
| V2 | Next | Evaluation and experiments |
| V3 | Planned | Failure Observatory |
| V4 | Planned | Productionization |
| V5 | Planned | Healthcare interoperability |

## Scope

The project is intentionally limited.

It does not currently include real patient data, autonomous clinical decisions, EHR integration, mobile/voice interfaces, fine-tuning, multi-agent systems, multiple medical domains, or Kubernetes.

## Tech direction

Python · FastAPI · PostgreSQL · pgvector · LLM provider abstraction · Docker · pytest

The stack will be introduced as the corresponding phases are implemented.

## License

Project license and contribution guidance will be added before the public release.
