# V4.2 PostgreSQL Persistence

V4.2 establishes the relational persistence boundary without changing V1–V3 domain contracts.

## Implemented

- SQLAlchemy database/session boundary.
- Relational models for documents, chunks, experiments, runs, answers, citations, evaluations, and failures.
- Initial SQL migration covering those entities and operational indexes.
- FailureRepository as the first domain-to-relational adapter.
- SQLite remains available for local development and repository tests.

## Production target

The same SQLAlchemy boundary is designed for PostgreSQL. The V4 deployment configuration will provide the PostgreSQL DATABASE_URL. pgvector is intentionally deferred to V4.3.

## Compatibility

The existing JSON FailureStore remains available for V3 compatibility. V4.2 does not silently replace it; the API/application layer can select the relational repository explicitly.
