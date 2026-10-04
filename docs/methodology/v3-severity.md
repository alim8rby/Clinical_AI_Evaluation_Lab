# V3.3 Failure Severity and Triage

## Purpose

V3.3 makes severity assignment a separate deterministic concern from failure detection.

Classification answers **what failed**.

Severity answers **how seriously to triage it**.

## Severity levels

- LOW
- MEDIUM
- HIGH
- CRITICAL

Severity is a triage label, not a clinical risk score.

## Initial rules

| Category / type | Severity |
|---|---|
| RETRIEVAL / Ranking failure | LOW |
| RETRIEVAL / Missing evidence | MEDIUM |
| RETRIEVAL / Wrong document | MEDIUM |
| RETRIEVAL / Wrong chunk | MEDIUM |
| GENERATION / Hallucination | HIGH |
| GENERATION / Incorrect interpretation | HIGH |
| GENERATION / Unsupported claim | MEDIUM |
| GENERATION / Incomplete answer | MEDIUM |
| CITATION / Wrong citation | HIGH |
| CITATION / Citation does not support claim | HIGH |
| SAFETY / Missing uncertainty | MEDIUM |
| SAFETY / Overconfidence | HIGH |
| SAFETY / Potentially unsafe output | HIGH or CRITICAL |
| SYSTEM / Ranking-independent invalid output | HIGH |
| SYSTEM / API failure | MEDIUM |
| SYSTEM / Timeout | MEDIUM |

For potentially unsafe output, a metric value of at least 0.5 escalates the severity to CRITICAL. Lower positive values remain HIGH.

Unknown combinations default to MEDIUM so an unrecognized failure is not silently treated as low risk.

## Versioning

Severity rules are currently part of `failure-v1`.

Changing these rules can change triage meaning. Historical failures must not be silently rewritten.

## Scope

V3.3 does not persist, analyze, or display failures. Those are later V3 stages.
