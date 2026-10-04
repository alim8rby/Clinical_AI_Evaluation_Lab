# V4.1 API Domain Adapters

V4.1 exposes the frozen domain through typed HTTP adapters.

## Implemented

- POST /api/v1/qa
- GET /api/v1/failures
- GET /api/v1/failures/{failure_id}
- GET /api/v1/failures/summary
- Pydantic request/response models
- Domain-to-API mapping for QA results and failure records
- Structured HTTP error responses

## Boundary

FastAPI routes contain transport concerns only. Failure filtering and summary logic remain in FailureObservatory. QA execution remains in ClinicalRAG.

The default QA dependency is intentionally unset until a production knowledge index and provider configuration are introduced. The API returns 503 rather than pretending that QA is available.

## Deferred

Experiment persistence, comparison APIs, run/evidence APIs, and production QA initialization depend on V4.2–V4.5 infrastructure.

## Compatibility

V4.1 does not modify V1–V3 domain contracts.
