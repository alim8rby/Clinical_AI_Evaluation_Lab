# V1.1 — Document Ingestion

## Scope

V1.1 implements the first executable stage of the controlled knowledge pipeline: converting one authoritative source into a normalized `Document` representation.

Initial domain: depression.

## Responsibilities

The ingestion module:

- accepts source content and required provenance metadata;
- validates required metadata and canonical HTTP(S) URLs;
- normalizes basic text formatting without changing clinical meaning;
- assigns a deterministic document identifier from stable source identity;
- preserves source provenance for downstream preprocessing.

## Deliberately excluded

V1.1 does not implement:

- PDF/HTML parsing;
- OCR;
- chunking;
- embeddings;
- vector storage;
- retrieval or ranking;
- LLM generation;
- database persistence;
- source discovery or web scraping.

## Contract

`ingest_document(...)` returns an immutable `SourceDocument` wrapped in an `IngestionResult`.

The normalized document preserves:

- `document_id`
- `title`
- `source`
- `organization`
- `publication_date`
- `url`
- `content`

`document_id` is deterministic for the same title, organization, and URL.

## Validation policy

Empty required metadata and empty content are rejected. URLs must be absolute HTTP(S) URLs. Text normalization is intentionally conservative: line endings, repeated whitespace, and excessive blank lines are normalized only.

## Freeze rule

This increment is complete when the ingestion implementation and unit tests establish the contract above. Changes that require parsing, chunking, storage, or additional source formats belong to later V1 increments rather than silently expanding V1.1.
