# V3.8 Failure Observatory UI

## Purpose

V3.8 adds the first user-facing Failure Observatory.

The UI is a presentation layer over the V3.7 query contract. It does not classify failures, assign severity, or persist records.

## Views

The initial screen provides:
- total failure count
- critical and high failure counts
- category distribution
- failure inventory
- category and severity filters
- selected-failure detail
- basic traceability context

## Data boundary

The frontend consumes a FailureObservatorySnapshot-shaped object containing failures and summary data.

The demo uses a local snapshot fixture because V3 deliberately has no HTTP API. The window.CAIELFailureObservatory.loadSnapshot() adapter allows the future API layer to replace that fixture without moving domain logic into the UI.

## Scope

Included:
- responsive static UI
- deterministic filtering
- failure detail
- summary distribution
- traceability presentation

Excluded:
- FastAPI
- authentication
- production data fetching
- database access
- classification logic
- severity logic
- deployment

## Design principle

The domain model and observatory service remain the source of truth. The frontend only renders the query contract.
