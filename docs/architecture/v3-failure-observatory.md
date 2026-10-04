# V3 Failure Observatory Architecture

## Goal

V3 turns V2 evaluation signals into a structured failure-analysis system.

V2 answers:

> How reliable was the system?

V3 answers:

> Where did it fail, what kind of failure was it, how severe was it, and can we prevent it from returning?

## Priority architecture decision

V3 remains local and UI-independent.

Do not introduce PostgreSQL, production APIs, authentication, deployment infrastructure, or other V4 concerns into V3.

The implementation order is:

1. Failure contract
2. Failure model
3. Deterministic classification
4. Severity
5. Local persistence
6. Failure analysis
7. Regression cases
8. Backend/query layer
9. UI
10. V3 audit and freeze

This keeps the failure-analysis domain stable before production infrastructure is introduced.

## Failure flow

```
Benchmark Question
       ↓
V1 RAG Run
       ↓
Answer + Evidence + Citations
       ↓
V2 Evaluation
       ↓
Evaluation Signals
       ↓
Failure Detection
       ↓
Failure Classification
       ↓
Severity
       ↓
Failure Record
       ↓
Persistence
       ↓
Analysis / Regression / Observatory
```

## Core traceability

Every failure must remain traceable to the run that produced it.

```
BenchmarkQuestion
       ↓
Run
       ↓
Answer
       ↓
Evaluation
       ↓
Failure
       ↓
Category / Type / Severity
       ↓
Evidence
```

Where available, analysis should also preserve the more detailed path:

```
Failure
  ↓
Metric signal
  ↓
Answer
  ↓
Claim
  ↓
Citation
  ↓
Chunk
  ↓
Document
```

A failure must never become a detached label without provenance.

## Failure taxonomy

V3 uses the existing project taxonomy.

### RETRIEVAL

- Missing evidence
- Wrong document
- Wrong chunk
- Ranking failure

### GENERATION

- Hallucination
- Incorrect interpretation
- Incomplete answer
- Unsupported claim

### CITATION

- Wrong citation
- Citation does not support claim

### SAFETY

- Overconfidence
- Missing uncertainty
- Potentially unsafe output

### SYSTEM

- API failure
- Timeout
- Invalid output

V3 may add a failure subtype only when implementation exposes a concrete gap in this taxonomy. New categories are not introduced casually.

## Failure record contract

A V3 failure record should contain:

- failure_id
- run_id
- answer_id when available
- question_id
- category
- type
- severity
- description
- evidence
- metric signal when available
- created_at
- classifier_version

The record must be serializable and reproducible.

## Failure detection vs classification

These are separate concerns.

**Detection** identifies a signal that something failed.

Examples:

- recall is zero
- citation is invalid
- unsupported claim rate is high
- recommendation claim has no citation
- run timed out

**Classification** converts that signal into the project taxonomy.

Example:

```
unsupported_claim_rate > threshold
        ↓
GENERATION / Hallucination
```

This separation allows detection rules and taxonomy mappings to evolve independently.

## Severity

Severity is a triage signal, not a clinical risk score.

Initial levels:

- LOW
- MEDIUM
- HIGH
- CRITICAL

Severity rules must be deterministic and documented.

They must not be presented as validated clinical safety classifications.

## Persistence boundary

V3 begins with a local structured store.

The persistence layer must:

- preserve stable IDs
- preserve provenance
- serialize deterministically
- support loading records
- avoid silent overwrites
- remain independent of UI code

PostgreSQL belongs to V4.

## Analysis boundary

Failure analysis operates on stored failure records and associated evaluation/run data.

It should support:

- counts by category
- counts by type
- counts by severity
- failure rates
- filtering by experiment
- filtering by benchmark question
- identifying recurring failures

Analysis must expose raw dimensions rather than collapsing them into a single score.

## Regression boundary

A known failure can become a regression case.

```
Known Failure
     ↓
Regression Case
     ↓
RAG Run
     ↓
Evaluation
     ↓
Pass / Fail
```

Regression cases should preserve the failure's original provenance and expected failure condition.

A fixed failure should therefore become a durable guard against recurrence.

## Observatory boundary

The query/backend layer is UI-independent.

Minimum query operations:

- list failures
- get failure
- filter by category
- filter by type
- filter by severity
- filter by experiment
- filter by question
- summarize failures

The UI consumes this boundary later. It must not contain classification or persistence logic.

## UI boundary

The V3 UI is intentionally downstream of the domain and query layers.

The first UI should support:

1. Failure summary
2. Failure list
3. Failure filters
4. Failure detail
5. Traceability to answer/evidence
6. Experiment/question context

No production authentication or deployment concerns belong here.

## Versioning and reproducibility

V3 records must preserve:

- classifier version
- source run
- benchmark version through the run/experiment
- failure classification
- severity rule version when introduced
- underlying metric signal where available

Changing a classification rule must not silently rewrite historical failure meaning.

## V2 compatibility

V2 remains frozen.

V3 consumes V2 evaluation results and adds failure-analysis behavior around them.

V3 must not change:

- V2 metric definitions
- benchmark semantics
- experiment comparison semantics
- V2 report semantics

If a concrete correctness problem is found, it requires an explicit documented decision.

## Explicit V3 exclusions

V3 does not include:

- PostgreSQL
- pgvector
- production API
- authentication
- deployment
- Kubernetes
- real patient data
- autonomous clinical decisions
- additional clinical domains
- fine-tuning
- multi-agent systems

## V3 acceptance criteria

V3 architecture is considered frozen when:

1. Failure records have a stable contract.
2. Detection and classification are separate.
3. Existing failure taxonomy remains the source of categories/types.
4. Severity is explicit and deterministic.
5. Failure provenance is preserved.
6. Local persistence is the initial storage boundary.
7. Analysis is independent from UI.
8. Regression cases can reference known failures.
9. UI consumes a backend/query boundary rather than embedding domain logic.
10. V2 remains frozen and compatible.

## Freeze rule

After V3.0, do not add architecture-level features casually.

If implementation exposes a concrete contract problem, document the problem, make the smallest justified correction, and record it in the V3 audit.
