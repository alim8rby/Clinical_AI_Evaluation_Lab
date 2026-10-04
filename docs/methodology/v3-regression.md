# V3.6 Failure Regression Suite

## Purpose

V3.6 protects the failure taxonomy and severity rules from silent behavioral changes.

The suite uses explicit regression cases with expected severity outcomes.

## Frozen cases

The initial suite covers:
- retrieval missing evidence
- retrieval ranking failure
- generation hallucination
- generation unsupported claim
- citation wrong citation
- safety missing uncertainty
- potentially unsafe output at the critical threshold
- potentially unsafe output below the critical threshold
- system timeout

Each case has a stable case ID and expected severity.

## Execution

run_regression_suite() evaluates every case against the current severity implementation.

assert_regression_suite() raises when any case deviates from its expected outcome.

The suite also accepts an alternate assigner in tests, which makes rule changes observable without mutating production code.

## Boundary

V3.6 does not:
- persist regression results
- classify live evaluation runs
- expose an API
- render the observatory
- replace the failure classifier

It is a deterministic guard around the existing severity contract.

## Versioning

Regression cases are part of the V3 failure-analysis contract. When severity rules intentionally change, the affected regression case and methodology version should be updated together rather than silently accepting a behavior change.
