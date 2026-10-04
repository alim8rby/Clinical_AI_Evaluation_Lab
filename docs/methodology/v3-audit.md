# V3 Audit and Freeze

## Status

**V3.0–V3.10: COMPLETE AND FROZEN**

Audit date: 2026-10-04.

## Contract audit

- Failure record has stable identity, run/question provenance, taxonomy, severity, evidence, metric signal, timestamp, and classifier version.
- Serialization is deterministic.
- Detection and classification remain separate.
- Severity is assigned by a deterministic rule set.
- Local persistence rejects conflicting ID reuse and performs atomic replacement.
- Analysis is read-only and deterministic.
- Observatory queries are UI-independent.
- The UI consumes the observatory-shaped snapshot rather than implementing domain logic.

## Classification audit

The classifier consumes existing V2 evaluation signals only.

Current rules cover:
- missing retrieval evidence
- invalid citations
- unsupported/hallucinated claims
- critical safety signals
- missing uncertainty
- unsupported recommendations

The taxonomy remains the V3 frozen taxonomy. No new category was introduced.

## Severity audit

Severity is explicit and deterministic across the frozen taxonomy.

It is documented as a triage signal, not a clinical risk score.

Known threshold behavior is protected by the regression suite, including the CRITICAL boundary for potentially unsafe output.

## Persistence audit

The JSON-backed FailureStore provides:
- stable IDs
- deterministic ordering
- round-trip serialization
- idempotent duplicate writes
- conflicting-ID protection
- invalid-store rejection
- atomic file replacement

PostgreSQL remains a V4 concern.

## Analysis and observatory audit

Analysis supports deterministic counts and exact filters by category, type, severity, run, and question.

The Observatory provides:
- list
- detail lookup
- filtering
- summary
- snapshot

The UI presents those results without classification, severity, or persistence logic.

## Regression audit

Known failure conditions are represented as frozen regression cases.

The integration suite explicitly runs the regression guard alongside the classification → persistence → observatory workflow.

## V2 compatibility audit

V3 does not change V2 metric definitions, benchmark semantics, experiment comparison semantics, or report semantics.

ExperimentResult.failures provides the existing V2-compatible retention boundary for recorded V3 failures.

## UI audit

V3.8 provides:
- failure summary
- category distribution
- failure inventory
- category/severity filters
- selected failure details
- traceability presentation

The current UI uses a local snapshot fixture because V3 has no HTTP API. A snapshot-loading adapter provides the boundary for future API integration.

## Known limitations

- Classification remains heuristic and deterministic.
- Severity is not clinically validated.
- Failure records do not yet carry a direct experiment_id; experiment context is available through the associated run in the current domain model.
- Observatory filtering is exact-field filtering; pagination, date ranges, trends, and full-text search are deferred.
- The UI is a local static presentation layer, not a production application.
- No local test execution is claimed by this audit; tests are present in the repository and this audit is based on source and contract inspection.

## Freeze decision

V3 is frozen.

Future changes to the V3 domain contracts require an explicit design decision. Production API, PostgreSQL/pgvector, authentication, deployment, and operational infrastructure begin in V4.
