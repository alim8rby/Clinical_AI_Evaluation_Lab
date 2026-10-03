# V1.7 — End-to-End RAG Pipeline

## Scope

V1.7 connects the completed V1 components into one executable pipeline:

Ingestion -> Chunking -> Vector Index -> Retrieval -> Generation -> Citation validation.

## Contract

ClinicalRAG.ingest(SourceDocument) returns Chunk records and adds them to the configured vector index.

ClinicalRAG.ask(question) returns RAGResult containing:

- question;
- retrieved chunks;
- EvidenceSet;
- structured Answer;
- validated Citation records.

## Boundary

The pipeline orchestrates existing module contracts. It does not introduce a second implementation of ingestion, chunking, retrieval, generation, or citation logic.

## Current development limitation

The pipeline uses the deterministic local embedding and mock generation implementations from V1.3 and V1.5. It is therefore an executable architecture and integration baseline, not yet a clinically meaningful RAG benchmark.

## Excluded

External LLM integration, production database infrastructure, automated evaluation, benchmark execution, API serving, and frontend UI remain outside V1.7.
