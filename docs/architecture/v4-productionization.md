# V4 Productionization Architecture

## Principle

V4 wraps the frozen V1–V3 domain with production infrastructure. The domain contracts remain the source of truth.

## Target shape

Browser → FastAPI → application/domain services → repositories/providers → PostgreSQL + pgvector / external model providers

The Failure Observatory UI consumes the API rather than owning domain logic.

## Layer boundaries

### API
HTTP concerns only: routing, request validation, response serialization, and error mapping.

### Application
Coordinates use cases: ask clinical question, execute experiment, evaluate run, inspect failures, compare experiments.

### Domain
Existing V1–V3 modules: ingestion, retrieval, generation, evaluation, experiments, and failure analysis.

### Infrastructure
External implementations: PostgreSQL, pgvector, model providers, embeddings, logging, and deployment.

## First implementation boundary

V4.0 introduces only the FastAPI application shell and health/error contract. It must not move domain logic into route handlers.

## Error contract

API errors use an error object with code, message, and details. Initial codes: INVALID_REQUEST, NOT_FOUND, RETRIEVAL_ERROR, GENERATION_ERROR, EVALUATION_ERROR, SYSTEM_ERROR.

## Health

GET /api/v1/health returns application status and safe environment information. It must not expose secrets or connection credentials.

## Production boundary

V4 infrastructure may depend on V1–V3 contracts, but V1–V3 modules should not depend on FastAPI, PostgreSQL, or deployment-specific code.
