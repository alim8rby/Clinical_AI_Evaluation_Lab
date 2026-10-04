# V2.4 Grounding and Citation Evaluation

## Purpose

V2.4 checks whether answer claims are cited and whether cited retrieved evidence contains support for those claims.

## Metrics

- Citation coverage: proportion of answer claims with at least one citation.
- Citation validity: proportion of answer claims with at least one citation resolving to retrieved evidence.
- Faithfulness: average claim-to-cited-evidence token overlap.
- Unsupported claim rate: 1 minus faithfulness.

## Important distinction

V1 citation validation checks referential correctness. V2.4 adds a deterministic support signal.

The support signal is an engineering baseline. Token overlap is not semantic entailment and does not establish clinical correctness.

## Contract

Input:
- Answer with structured claims
- Citation records
- EvidenceSet containing retrieved chunks

Output:
- claim-level grounding metrics
- evaluator version

Invalid citations reduce citation validity. Uncited claims reduce coverage and contribute zero support.

## Future extension

A model-assisted semantic entailment evaluator may replace or complement token overlap behind the same evaluation boundary. Such an evaluator must record its model and evaluator configuration.

V2.4 does not add an external judge dependency.
