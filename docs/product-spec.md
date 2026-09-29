# Product Specification v1.0

## Purpose
Build an evidence-grounded clinical question-answering system and a controlled environment for measuring reliability, performance, and failure modes.

## Initial domain
Depression.

## Primary user
AI/ML engineer working on healthcare AI.

## Core journey
Open Lab -> Choose configuration -> Ask question -> Retrieve evidence -> Generate answer -> Inspect evidence/citations -> Evaluate -> Inspect failures -> Compare experiments.

## Screens
1. Overview
2. Clinical QA
3. Evidence Explorer
4. Evaluation Lab
5. Experiment Comparison
6. Failure Observatory

## Evaluation dimensions
### Retrieval
Precision@K, Recall@K, MRR, nDCG

### Generation
Correctness, Completeness, Relevance

### Grounding
Faithfulness, Citation correctness, Unsupported claim rate

### Reliability
Hallucination rate, Critical error rate, Uncertainty handling, Unsupported recommendation rate

### Operations
Latency, Token usage, Cost, Failure rate

## Failure taxonomy
- Retrieval: missing evidence, wrong document, wrong chunk, ranking failure
- Generation: hallucination, incorrect interpretation, incomplete answer, unsupported claim
- Citation: wrong citation, citation does not support claim
- Safety: overconfidence, missing uncertainty, potentially unsafe output
- System: API failure, timeout, invalid output

## Out of V1
General medical knowledge, real patient data, autonomous clinical decisions, EHR integration, mobile app, voice interface, fine-tuning, multi-agent architecture, FHIR implementation, Kubernetes, complex authentication, multiple medical domains.
