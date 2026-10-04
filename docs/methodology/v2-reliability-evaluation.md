# V2.5 Reliability Evaluation

## Purpose

V2.5 converts grounding and answer structure into explicit reliability signals.

## Metrics

- Hallucination rate: inherited unsupported-claim rate.
- Critical error rate: deterministic safety-sensitive signal when safety-related language is substantially unsupported.
- Uncertainty handling: whether the answer records uncertainty when appropriate.
- Unsupported recommendation rate: proportion of recommendation-like claims without citation references.

## Important limitation

These are conservative engineering signals, not a clinical safety classifier.

In particular:
- unsupported claim rate is a proxy for hallucination;
- keyword-based critical-error detection can miss or over-flag clinical situations;
- recommendation detection is pattern-based;
- uncertainty quality is not equivalent to calibrated uncertainty.

Reliability results must therefore be interpreted alongside the underlying answer, evidence, citations, and failure taxonomy.

## Failure taxonomy mapping

Reliability signals may map to:
- GENERATION / Hallucination
- SAFETY / Overconfidence
- SAFETY / Missing uncertainty
- SAFETY / Potentially unsafe output
- CITATION / Citation does not support claim

The evaluator records signals; failure classification remains a separate concern.

## Contract

Input:
- Answer
- GroundingMetrics

Output:
- structured ReliabilityMetrics
- evaluator version

No external model or API dependency is introduced.
