# V2.6 Experiment Tracking

## Purpose

V2.6 records the configuration and run identity needed to reproduce evaluation results.

## Experiment configuration

Each experiment captures:

- model configuration
- embedding configuration
- retriever configuration
- top-k
- prompt version
- benchmark version

The configuration is immutable after construction.

## Experiment identity

Experiment IDs are deterministic hashes of the experiment definition. This gives equivalent definitions the same identity and makes configuration drift visible.

Creation time is metadata and is not part of the experiment identity.

## Run record

Each run records:

- run ID
- experiment ID
- benchmark question ID
- status
- timestamps
- latency
- input/output tokens
- cost
- error

Operational fields may be unavailable and are therefore nullable.

## Result linkage

ExperimentResult groups a run with retrieval, answer, grounding, and reliability results.

This keeps evaluation outputs traceable without introducing persistence infrastructure.

## Scope

V2.6 does not add PostgreSQL, ORM, API endpoints, or a UI. Those belong to later product phases.
