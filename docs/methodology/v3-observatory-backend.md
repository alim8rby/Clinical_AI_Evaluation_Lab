# V3.7 Failure Observatory Backend

## Purpose

V3.7 provides the read-oriented query layer that the future Failure Observatory UI can consume.

It composes the V3.4 persistence and V3.5 analysis layers instead of duplicating their behavior.

## Operations

- Get one failure by stable ID.
- List failures using exact category, type, severity, run, and question filters.
- Apply a deterministic result limit.
- Produce filtered summaries.
- Produce a combined snapshot containing failures and summary data.

Results are ordered by stable failure ID.

## Boundary

The observatory service is UI-independent.

It does not:
- expose HTTP routes
- render HTML or frontend components
- mutate failures
- classify failures
- assign severity
- connect to PostgreSQL
- introduce authentication

The API layer remains a later infrastructure concern.

## Design

The service accepts a FailureStore dependency. This keeps storage replaceable and makes the observatory query contract independent of the current JSON implementation.

FailureNotFoundError provides a domain-level not-found result for future API adapters.

## Limitations

The initial query model uses exact filters only. Full-text search, pagination, date ranges, trend analysis, and production database queries remain future work.
