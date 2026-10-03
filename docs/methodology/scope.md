# Scope and Methodology

## V0 scope

V0 establishes the product boundary, repository architecture, data model direction, and module/API contracts.

## V1 scope

V1 will implement a working evidence-grounded RAG system for depression.

It will include:

- controlled document ingestion
- preprocessing and chunking
- provenance metadata
- embeddings and retrieval
- answer generation
- citations

## Explicit exclusions

The initial release does not include:

- real patient data
- autonomous clinical decisions
- EHR integration
- mobile applications
- voice interfaces
- fine-tuning
- multi-agent architecture
- FHIR implementation
- Kubernetes
- complex authentication
- multiple clinical domains

## Methodological principle

Every evaluation result must be reproducible from a defined configuration, benchmark, model, retriever, and recorded run.
