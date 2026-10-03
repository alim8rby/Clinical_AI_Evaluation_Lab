# V1.2 — Document Preprocessing & Chunking

## Scope

V1.2 converts an ingested SourceDocument into ordered, retrievable Chunk records.

## Responsibilities

- normalize basic whitespace and line endings;
- preserve paragraph boundaries where possible;
- combine sentences up to a deterministic character limit;
- split oversized sentences into fixed character windows;
- assign deterministic chunk identifiers;
- preserve document_id, chunk order, section, and page fields.

## Excluded

PDF/HTML parsing, OCR, semantic chunking, overlap strategies, embeddings, vector storage, retrieval, ranking, and database persistence.

## Contract

chunk_document(document, max_chars=...) returns an ordered list of Chunk records.

chunk_index starts at zero and increases monotonically. chunk_id is deterministic for the same document identity, position, and text.

## Provenance

document_id is copied unchanged into every chunk. section and page remain nullable for later format-specific parsers.

## Freeze rule

Parsing, richer structural metadata, semantic chunking, overlap strategies, embeddings, and retrieval belong to later increments.
