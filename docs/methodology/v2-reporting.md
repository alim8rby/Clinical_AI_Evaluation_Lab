# V2.8 Evaluation Reporting

## Purpose

V2.8 turns recorded experiment results into a reproducible evaluation report.

## Report contents

1. Experiment identity.
2. Benchmark version.
3. Configuration snapshot.
4. Number of evaluated samples.
5. Aggregated evaluation metrics.
6. Recorded failures.

Metrics are arithmetic means over supplied result records. Missing metric groups remain missing rather than becoming zero.

The report is generated only from recorded Experiment and ExperimentResult objects. It does not call an external model, infer missing results, or silently add scores.

The current renderer produces Markdown so reports remain inspectable in Git and can later feed a UI or richer reporting layer.

## Scope

V2.8 does not add persistence, dashboards, or deployment.
