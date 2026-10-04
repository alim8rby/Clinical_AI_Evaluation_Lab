# V3.4 Failure Persistence

## Purpose

V3.4 adds a small local persistence boundary for structured failure records.

The store is intentionally independent of the API, UI, and production database.

## Storage format

Failures are stored as a JSON list.

Each record uses the existing Failure.to_dict() representation. Records are sorted by failure_id before writing so the file is deterministic and easy to inspect in versioned development environments.

## Write behavior

- New failure IDs are appended and persisted.
- Re-saving the exact same failure is idempotent.
- Reusing an ID with different content is rejected.
- Writes use a temporary file followed by replacement to avoid leaving a partially written store on normal write failure.

## Read behavior

- A missing store is treated as empty.
- Records are reconstructed through failure_from_dict().
- Invalid JSON, a non-list root, or an invalid record raises FailureStoreError.
- Reads return failures in deterministic ID order.

## Boundary

FailureStore owns local persistence only.

It does not:
- classify failures
- assign severity
- expose an HTTP API
- render UI
- connect to PostgreSQL
- rewrite historical failures

PostgreSQL/pgvector and production persistence remain V4 concerns.

## Reproducibility

The persisted representation uses the existing stable failure IDs and deterministic JSON ordering. The store therefore preserves failure records without introducing database-generated identifiers.

## Limitations

This is a local development persistence layer, not a concurrent multi-process database. V4 can replace it behind the same conceptual persistence boundary when production infrastructure is introduced.
