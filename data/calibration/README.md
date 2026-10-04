# Semantic Evaluator Calibration

This directory stores human-reviewed calibration labels for the model-assisted
semantic evaluator.

Human review is an annotation exercise, not clinical validation. Reviewers
should score only the supplied benchmark question, reference answer, key
concepts, answer, claims, and evidence.

## Dimensions

- correctness
- completeness
- relevance
- faithfulness
- unsupported_claim_rate

Scores are continuous values from 0 to 1.

## Annotation rules

1. Review the supplied material only.
2. Do not add outside clinical facts.
3. Score correctness against the reference answer.
4. Score completeness against the key concepts and reference answer.
5. Score relevance against the question.
6. Score faithfulness only against the supplied evidence.
7. Score unsupported_claim_rate as the proportion of answer content that is not supported by the supplied evidence.
8. Record uncertainty in reviewer notes rather than silently resolving ambiguity.

The first calibration set should be manually reviewed before any agreement
result is presented as evidence about evaluator quality.

See docs/methodology/v5.1-calibration.md.
