# V3.5 Failure Analysis

## Purpose

V3.5 adds deterministic analysis operations over persisted failure records.

The analysis layer answers:
- Which failures match a set of exact filters?
- How many failures exist by category?
- How many failures exist by failure type?
- How many failures exist by severity?

## Operations

### Filtering

filter_failures() supports exact matching on category, failure type, severity, run ID, and question ID. Multiple filters use AND semantics. Results are returned in stable failure_id order.

### Summaries

FailureSummary contains total failure count, counts by category, counts by type, and counts by severity. Count maps use deterministic key ordering.

### Store analysis

analyze_store() combines store loading, filtering, and summarization without adding a persistence concern to the analysis module.

## Boundary

V3.5 does not classify new failures, change severity, mutate stored failures, expose an HTTP API, render the observatory UI, connect to PostgreSQL, or calculate a composite reliability score.

The analysis layer is intentionally UI-independent so the future Failure Observatory can consume it.

## Limitations

Analysis is descriptive rather than causal. It summarizes recorded failures but does not infer why a failure occurred beyond the evidence already attached to the record.

Future V3 stages can build regression and observatory query workflows on these stable operations.
