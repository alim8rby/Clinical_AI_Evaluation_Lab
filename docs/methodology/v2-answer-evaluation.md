# V2.3 Answer Evaluation

## Purpose

V2.3 measures answer quality against the ClinicalQA-v1 reference answer and key concepts.

## Metrics

- Correctness: token-level overlap with the reference answer.
- Completeness: proportion of benchmark key concepts explicitly present in the answer.
- Relevance: proportion of answer tokens that also occur in the reference answer.

All scores are normalized to 0–1.

## Contract

Input:
- validated BenchmarkQuestion
- generated Answer

Output:
- question ID
- correctness
- completeness
- relevance
- evaluator version

The evaluator consumes the project Answer model, not provider SDK objects.

## Important limitation

These are deterministic engineering baselines, not clinical semantic judgement. Token overlap can miss paraphrases and can reward shared wording without understanding meaning.

A future model-assisted evaluator may implement the same evaluator boundary, but must record its model, prompt/version, and evaluation configuration.

## Scope

V2.3 does not introduce an LLM judge, external API dependency, or clinical decision logic.
