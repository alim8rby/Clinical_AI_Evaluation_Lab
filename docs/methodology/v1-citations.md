# V1.6 — Citation & Traceability

## Scope

V1.6 converts claim evidence references from an Answer into explicit Citation records.

## Contract

build_citations(answer, evidence, answer_id) returns Citation records linking:

Claim -> Citation -> Chunk -> Document

Every claim must contain at least one valid one-based evidence index. An invalid or missing reference is rejected rather than silently producing an unsupported citation.

## Traceability

The Citation stores answer identity, claim index, and chunk identity. The chunk already preserves document identity, so the complete source chain remains resolvable.

## Excluded

V1.6 does not evaluate whether the cited chunk actually supports the claim. Citation correctness is an evaluation concern for V2.
