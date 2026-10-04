# V2.2 Retrieval Evaluation

## Purpose

V2.2 measures whether retrieval returns the evidence expected by ClinicalQA-v1.

## Metrics

For a question with expected evidence set E and retrieved list R at cutoff K:

- Precision@K = relevant retrieved items / K
- Recall@K = relevant retrieved items / |E|
- MRR = reciprocal rank of the first relevant retrieved item
- nDCG@K = normalized discounted cumulative gain using binary relevance

Expected evidence is defined by stable chunk IDs. No semantic similarity or model judgement is used by these metrics.

## Contract

Input:
- validated BenchmarkQuestion
- EvidenceSet from the V1 retriever
- cutoff K

Output:
- question ID
- retrieved chunk IDs
- expected chunk IDs
- structured RetrievalMetrics

The evaluator rejects empty expected evidence, invalid K, and duplicate retrieved IDs.

## Interpretation

These metrics measure retrieval against the benchmark's evidence mapping. They do not establish clinical correctness, answer quality, citation correctness, or safety.

A benchmark question must pass the V2.1 evidence gate before retrieval scoring.

## Reproducibility

Metric calculations are deterministic from retrieved IDs, expected IDs, and K.
