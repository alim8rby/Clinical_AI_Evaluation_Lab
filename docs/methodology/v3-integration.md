# V3.9 Failure Analysis Integration

## Purpose

V3.9 connects the V3 failure-analysis components into one local workflow:

1. Receive a completed V2 evaluation result.
2. Classify detected failure signals.
3. Assign deterministic severity.
4. Persist failure records.
5. Retain serialized failures on the experiment result.
6. Expose the persisted records through the Failure Observatory query boundary.

## Integration boundary

The workflow is implemented in `src/failure_analysis/workflow.py`.

It depends on the existing:
- V2 `BenchmarkQuestion` and `ExperimentResult`
- V3 classifier
- V3 severity engine
- V3 local `FailureStore`
- V3 `FailureObservatory`

It does not add:
- HTTP endpoints
- PostgreSQL
- authentication
- deployment infrastructure

## Idempotency

Failure IDs are deterministic from run, category, and type. Reprocessing the same result therefore produces the same failure records and is safe against duplicate writes.

Conflicting reuse of a failure ID remains rejected by `FailureStore`.

## Result retention

The workflow updates the returned `ExperimentResult` with serialized failure records. This keeps V2 report generation compatible with V3 failure data without changing V2 metric definitions.

## UI boundary

The Failure Observatory UI remains downstream. It can consume a snapshot produced by `build_observatory(store)` without knowing how failures were detected or stored.

## Acceptance criteria

- One evaluated result can flow through classification and persistence.
- Failure records retain run/question/metric provenance.
- Reprocessing is idempotent.
- Observatory queries see persisted failures.
- V2 result/report structures remain compatible.
