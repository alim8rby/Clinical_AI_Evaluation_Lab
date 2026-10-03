# V2 Evaluation Architecture

## Goal

V2 turns the V1 RAG pipeline into a controlled evaluation system.

The core question is:

> Given the same benchmark, how well does a configured RAG system retrieve evidence, answer questions, stay grounded, and handle uncertainty?

V2 does not change the V1 RAG path. It evaluates it.

## Scope

V2 covers:

- ClinicalQA-v1 benchmark
- Retrieval evaluation
- Answer evaluation
- Grounding and citation evaluation
- Reliability evaluation
- Experiment tracking
- Experiment comparison
- Reproducible evaluation reports

V2 does not add:

- Production API
- PostgreSQL or pgvector
- Frontend UI
- Authentication
- Deployment
- Real patient data
- Multiple clinical domains
- Fine-tuning
- Multi-agent systems

## Evaluation flow

```text
Benchmark Question
       ↓
Experiment Configuration
       ↓
RAG Run
       ↓
Answer + Evidence + Citations
       ↓
Evaluation
       ↓
Metrics + Failures
```

## Benchmark contract

Each BenchmarkQuestion must contain:

- question_id
- question
- domain
- difficulty
- expected_evidence
- reference_answer
- key_concepts

The initial benchmark is depression-only.

Benchmark size:
- V2.1 seed set: 30–50 questions
- V2 target: 100–300 questions

The seed set is for building and checking the evaluation system. It is not presented as a statistically representative clinical benchmark.

## Metric groups

### Retrieval
- Precision@K
- Recall@K
- MRR
- nDCG

Retrieval metrics operate on retrieved chunk IDs and expected evidence IDs.

### Answer quality
- Correctness
- Completeness
- Relevance

The evaluator interface must allow deterministic evaluators first and model-assisted evaluators later.

### Grounding
- Faithfulness
- Citation correctness
- Unsupported claim rate

The evaluation must distinguish:
1. Citation exists.
2. Citation points to retrieved evidence.
3. Evidence actually supports the claim.

V1 currently handles the first two. V2 adds the third.

### Reliability
- Hallucination rate
- Critical error rate
- Uncertainty handling
- Unsupported recommendation rate

Reliability findings can be mapped to the existing failure taxonomy.

### Operations
V2 may record available latency, token usage, cost, and failure status. This does not expand the V1 runtime.

## Evaluator contract

Evaluators accept explicit domain objects and return structured results.

```text
Evaluator
  input:
    benchmark question
    answer
    evidence
    citations
    configuration
  output:
    metric results
    details
    optional failures
```

Provider-specific SDK objects must not cross the evaluation boundary.

## Metric result

Each result identifies:
- metric name
- value
- unit or interpretation
- evaluator version
- supporting details

Results must be reproducible from recorded inputs and configuration.

## Experiment contract

An experiment captures:
- experiment ID
- name
- model configuration
- embedding configuration
- retriever configuration
- top-k
- prompt version
- benchmark version
- creation metadata

Comparisons use the same benchmark version unless the difference is explicitly documented.

## Reproducibility

V2 preserves:
- benchmark version
- experiment configuration
- prompt version
- model/provider identifiers
- retriever settings
- evaluator version
- records needed to inspect results

Changing defaults must not silently change historical experiment results.

## Comparison

Experiment comparison returns measurements by experiment and metric, including:
- metric values
- metric differences
- sample counts
- relevant configuration

The comparison layer does not collapse all dimensions into one hidden score.

## Reporting

A V2 report should answer:
1. What system was evaluated?
2. Which benchmark was used?
3. How was it configured?
4. What were the retrieval results?
5. What were the answer, grounding, and reliability results?
6. Which failures occurred?
7. What changed between compared experiments?

## Acceptance criteria

V2 is complete when the repository can:

1. Load a versioned ClinicalQA-v1 benchmark.
2. Run the frozen V1 RAG pipeline against benchmark questions.
3. Produce structured evaluation results.
4. Calculate retrieval metrics.
5. Evaluate answer quality.
6. Evaluate grounding and citation support.
7. Record reliability findings.
8. Store experiment configuration.
9. Compare experiments on the same benchmark.
10. Produce a reproducible evaluation report.
11. Preserve question → run → answer → evaluation → failure traceability.

## V2 freeze rule

Do not add production infrastructure or UI work to V2.

If implementation exposes a concrete V1 contract problem, document and fix it explicitly. Otherwise V1 remains frozen.
