# Architecture

## System flow
User -> Query Processor -> Retriever -> Evidence Set -> LLM -> Structured Answer -> Evaluation -> Storage

## Knowledge flow
Authoritative documents -> parsing -> cleaning -> chunking -> metadata -> embeddings -> vector storage -> retrieval

## Retrieval
The retrieval layer will support dense search, keyword search, and reranking.

## AI abstraction
Generation must support multiple model providers without coupling the application to a single model.

## Traceability
Generated claims should remain traceable to retrieved evidence where applicable.
