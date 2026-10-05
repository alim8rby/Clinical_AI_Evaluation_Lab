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

## V5.3 — Retrieval Research Layer — ENGINEERING COMPLETE
- Dense retrieval research baseline
- Deterministic BM25 retrieval
- Hybrid dense + BM25 retrieval
- Shared benchmark-facing evaluation contract
- Precision@K, Recall@K, MRR, nDCG, and latency comparison
- Cross-strategy comparison report
- V4 production retrieval path unchanged
- Methodology and limitations documented

Empirical benchmark runs remain environment-dependent and should not be represented as completed results until executed.

## V5.4 — Generation Evaluation Layer — ENGINEERING COMPLETE
- Controlled generation-provider experiments
- Fixed benchmark and evidence conditions
- Quality, grounding, reliability, latency, token, and cost comparisons
- Question-level result retention
- Cross-provider summaries
- No hidden composite score
- Methodology and audit completed

Empirical model-performance results remain pending an executed controlled benchmark run.

## V5.5 — Experiment Engine — ENGINEERING COMPLETE
- Reproducible sequential batch benchmark runs
- Experiment configuration snapshots
- Continue-on-error and explicit stop-on-error modes
- Question-level result and execution-error retention
- Aggregate evaluation reports
- Existing failure retention preserved
- Methodology and audit completed

Empirical benchmark runs remain pending actual execution.

## V5.6 — Statistical Evaluation — ENGINEERING COMPLETE
- Question-level paired comparisons
- Deterministic bootstrap confidence intervals
- Paired standardized effect sizes
- Experiment-level statistical comparison reports
- Explicit uncertainty-aware interpretation
- No hidden composite quality score
- No clinical-superiority claim
- Methodology and audit completed

Empirical statistical results remain pending actual experiment execution.

## V5.7 — Failure Observatory 2.0 — ENGINEERING COMPLETE
- Experiment-aware failure trends
- Failure analysis by category, type, severity, difficulty, and question type
- Unique affected-question counts
- Baseline/candidate failure-rate comparison
- Configurable regression signals
- Frozen V3 failure schema preserved
- Methodology and audit completed

Empirical regression results remain pending actual experiment execution.

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
