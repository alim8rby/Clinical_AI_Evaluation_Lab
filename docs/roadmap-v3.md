# V3 Roadmap — Failure Observatory

## Goal

Turn V2 evaluation signals into a structured system for classification, inspection, analysis, and regression testing.

## Priority recommendation

Keep V3 local and UI-independent until the failure domain is stable.

**Do not introduce PostgreSQL, production APIs, authentication, deployment, or other V4 infrastructure during V3.**

## V3.0 — Failure Architecture & Scope — COMPLETE

- Freeze failure contract
- Freeze taxonomy boundary
- Separate detection from classification
- Define severity
- Define provenance
- Define persistence boundary
- Define analysis/query boundary
- Define regression boundary
- Define UI boundary
- Define V2 compatibility rules

## V3.1 — Failure Data Model — NEXT

- Failure dataclass
- Severity model
- Validation
- Serialization contract
- Unit tests

## V3.2 — Failure Classification Engine

- Deterministic detection signals
- Taxonomy mapping
- Classifier versioning
- Unit tests

## V3.3 — Failure Severity & Triage

- Deterministic severity rules
- Severity rationale
- Tests

## V3.4 — Failure Persistence

- Local structured result store
- Stable IDs
- Deterministic serialization
- Loading and overwrite protection

## V3.5 — Failure Analysis

- Category/type/severity counts
- Failure rates
- Experiment/question filters
- Recurring failure analysis

## V3.6 — Failure Regression Suite

- Regression case model
- Known-failure fixtures
- Pass/fail evaluation
- Recurrence protection

## V3.7 — Failure Observatory Backend

- Failure query layer
- Filtering
- Detail retrieval
- Summaries

## V3.8 — Failure Observatory UI

- Summary
- Failure list
- Filters
- Failure detail
- Traceability

## V3.9 — V3 Integration

- End-to-end V2 → failure pipeline
- Persistence
- Analysis
- Regression
- Observatory

## V3.10 — V3 Audit & Freeze

- Contract audit
- Classification audit
- Severity audit
- Persistence audit
- Regression audit
- UI/backend boundary audit
- V2 compatibility audit
- Documentation and tests
- Freeze V3
