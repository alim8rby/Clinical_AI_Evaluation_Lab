# V4.0 Production API Foundation

V4.0 adds the FastAPI application shell around the frozen V1–V3 domain.

## Included

- FastAPI application entry point
- /api/v1 route boundary
- health endpoint
- environment settings boundary
- structured invalid-request errors
- generic system-error contract
- API integration tests

## Boundary

The routes currently contain no RAG, evaluation, failure classification, persistence, or provider logic. Those concerns remain in the existing domain modules and will be connected through application adapters in V4.1.

## Configuration

Safe defaults are:
- APP_ENV=development
- APP_HOST=127.0.0.1
- APP_PORT=8000
- LOG_LEVEL=INFO

Secrets and database credentials remain environment-only.

## Freeze rule

V4.0 does not add database models, real LLM providers, authentication, deployment, or business logic to route handlers.
