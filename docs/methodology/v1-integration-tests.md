# V1.8 — Integration & Reliability Tests

## Scope

V1.8 verifies the executable boundary assembled in V1.7 without introducing new runtime behavior.

## Covered paths

The integration suite verifies:

1. Successful end-to-end execution from document ingestion to traceable citations.
2. Empty questions are rejected before generation.
3. Invalid retrieval limits are rejected.
4. An empty knowledge index cannot silently produce an answer.
5. Invalid provider citation references are rejected by the citation boundary.

## Reliability principle

The pipeline must fail explicitly when a required prerequisite or traceability contract is violated. Tests therefore assert controlled exceptions rather than accepting partial or silently ungrounded output.

## Verification status

The repository contains deterministic integration tests using the local development index and mock generation provider. This phase is source-verified in GitHub; local test execution is not claimed here.

## Excluded

External model calls, production databases, benchmark scoring, API deployment, and UI behavior remain outside V1.
