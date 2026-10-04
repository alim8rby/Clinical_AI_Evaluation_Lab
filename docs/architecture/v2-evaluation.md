# V2 Evaluation Architecture

## Result

V2 is the frozen evaluation layer for the V1 RAG system.

## Scope

V2 covers the ClinicalQA-v1 benchmark, retrieval, answer, grounding, reliability, experiment tracking, comparison, and reproducible reports. It excludes production API, database, frontend, authentication, deployment, real patient data, multiple domains, fine-tuning, and multi-agent systems.

## Evaluation flow

Benchmark Question → Experiment Configuration → RAG Run → Answer + Evidence + Citations → Evaluation → Metrics + Failures

## Benchmark

The current benchmark is depression-only with eight engineering-seed questions. Evidence mappings resolve to stable controlled-corpus chunk IDs. Planned growth is 30–50 questions, then 100–300.

## Metrics

Retrieval: Precision@K, Recall@K, MRR, nDCG.

Answer: Correctness, Completeness, Relevance.

Grounding: Citation coverage, Citation validity, Faithfulness, Unsupported claim rate.

Reliability: Hallucination proxy, Critical-error signal, Uncertainty handling, Unsupported recommendation rate.

## Reproducibility

Experiment configuration records model, embedding, retriever, top-k, prompt version, and benchmark version. Run records preserve operational metadata. Failures are retained in ExperimentResult. Reports use only recorded project data.

## Freeze rule

No production infrastructure or UI work is added to V2. Later changes require a documented concrete correctness issue.
