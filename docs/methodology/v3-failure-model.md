# V3.1 Failure Data Model

## Purpose

V3.1 turns the V3 failure contract into typed Python domain objects.

## Failure

A failure records a concrete problem detected during a run.

Required fields:

- failure_id
- run_id
- question_id
- category
- type
- severity
- description
- evidence
- classifier_version

Optional fields:

- answer_id
- metric
- metric_value
- created_at

## Severity

The initial severity enum is:

- LOW
- MEDIUM
- HIGH
- CRITICAL

Severity is a triage label, not a validated clinical risk score.

## Serialization

Failures support deterministic dictionary and JSON serialization.

Deserialization validates required fields and converts severity and timestamps back to their domain types.

The model does not persist records itself. Storage belongs to V3.4.

## Validation

Required string fields must be non-empty.

Severity must use the FailureSeverity enum.

Metric values, when present, must be numeric.

The model does not validate taxonomy membership yet. Taxonomy classification belongs to V3.2.

## Versioning

The default classifier version is `failure-v1`.

Historical failure meaning must not be silently rewritten when future classification rules change.
