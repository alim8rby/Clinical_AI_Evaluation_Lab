# V4.4 Ollama Provider Integration

CAIEL now supports local Ollama behind provider-neutral interfaces.

Default local configuration:
- Generation: `llama3.2:3b`
- Embeddings: `nomic-embed-text`
- Ollama: `http://127.0.0.1:11434`

Generation returns the existing `Answer` contract and requests structured JSON containing answer text, uncertainty, claims, and citation indices.

Embedding returns a plain vector through `EmbeddingProvider`.

Timeouts and HTTP/provider failures are converted into explicit runtime errors rather than leaking provider-specific exceptions into the domain layer.

The deterministic local embedding provider remains available for V1/V3 regression compatibility.

The Ollama embedding vector dimension must match the PostgreSQL pgvector column. The current V4.3 migration remains 256-dimensional; production activation with `nomic-embed-text` requires a dimension-aligned migration before indexing those embeddings.
