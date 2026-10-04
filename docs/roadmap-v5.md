# V5 Roadmap — Evaluation Platform

V5 upgrades CAIEL from a productionized clinical RAG demo into a stronger evaluation platform. The phase prioritizes evaluator calibration, benchmark quality, controlled retrieval/generation experiments, reproducibility, and failure analysis.

## V5.1 — Evaluation Calibration — ENGINEERING COMPLETE
- Versioned human-label schema
- Explicit annotation rubric
- Calibration agreement metrics: MAE, mean bias, within-tolerance rate
- Controlled empty calibration dataset scaffold
- Validation and integration tests
- Production evaluator behavior unchanged
- Human-reviewed labels remain a manual research step

## V5.2 — Benchmark v2 — FROZEN
- Separate versioned ClinicalQA-v2 contract
- 60-question benchmark: frozen 40-question v1 baseline + 20-question expansion
- Explicit question-type metadata
- Explicit safety-relevance metadata
- Controlled-corpus evidence validation
- Coverage audit and versioning policy
- V5.2 audit and freeze

## V5.3 — Retrieval Research Layer — PLANNED
- Dense, BM25, and hybrid retrieval comparisons
- Optional reranking experiments
- Retrieval metrics and latency comparison

## V5.4 — Generation Evaluation Layer — PLANNED
- Controlled multi-model experiments
- Consistent evidence and benchmark conditions
- Quality, grounding, reliability, latency, token, and cost comparisons

## V5.5 — Experiment Engine — PLANNED
- Reproducible batch benchmark runs
- Experiment configuration capture
- Aggregate results and failure retention

## V5.6 — Statistical Evaluation — PLANNED
- Question-level paired comparisons
- Confidence intervals
- Effect sizes and uncertainty-aware reporting
- No hidden composite quality score

## V5.7 — Failure Observatory 2.0 — PLANNED
- Failure trends by experiment, model, difficulty, and question type
- Regression detection
- Experiment-to-failure-to-evidence traceability

## V5.8 — Evidence Explorer 2.0 — PLANNED
- Full Question → Evidence → Claim → Citation → Chunk → Document inspection
- Retrieved-but-unused evidence
- Claim support inspection

## V5.9 — Reproducible Model Configuration — PLANNED
- Explicit model, embedding, retriever, prompt, evaluator, and benchmark versions
- Reproducible experiment configuration

## V5.10 — Platform UX — PLANNED
- Experiment workflow
- Metric exploration
- Comparison views
- Failure investigation workflow

## V5.11 — Research Reports — PLANNED
- Durable experiment reports
- Methodology and limitation summaries
- Reproducible result artifacts

## V5.12 — V5 Audit & Freeze — PLANNED
- Methodology audit
- Reproducibility audit
- Security and operational review
- Documentation and limitation review
- V5 freeze

## Explicit exclusions
V5 does not add real patient data, autonomous clinical decisions, FHIR/EHR integration, multi-agent architecture, fine-tuning, Kubernetes, or additional clinical domains unless a later scope decision explicitly reopens them.
