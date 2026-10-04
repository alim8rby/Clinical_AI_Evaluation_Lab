# V2.7 Experiment Comparison

## Purpose

V2.7 compares two experiment configurations on the same benchmark.

## Rules

- Baseline and candidate must be different experiments.
- Both must use the same benchmark version.
- Metrics are averaged across the supplied completed results.
- Only metrics present in both experiments are compared.
- The comparison exposes the raw baseline, candidate, delta, and sample counts.

## No hidden score

The comparison does not create a composite score. Retrieval, answer quality, grounding, reliability, and operational metrics remain separate so trade-offs are visible.

## Configuration

Experiment IDs identify the configurations. The caller can inspect each ExperimentConfig to understand model, embedding, retriever, top-k, prompt, and benchmark differences.

## Limitation

V2.7 currently compares supplied in-memory results. Persistence and API exposure are deferred to later phases.
