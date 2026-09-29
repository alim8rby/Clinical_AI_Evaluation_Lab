# Data Model

## Core entities
Document
Chunk
BenchmarkQuestion
Experiment
Run
Answer
Citation
Evaluation
Failure

## Relationships
Document -> Chunk
Experiment -> Run -> Answer
Answer -> Citation
Answer -> Evaluation
Answer -> Failure
BenchmarkQuestion -> Run
