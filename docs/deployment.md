# Deployment

## CI

GitHub Actions runs on pushes and pull requests:

1. Install Python dependencies.
2. Compile Python sources.
3. Run the repository pytest suite.
4. Run Ruff static analysis.
5. Build the Docker image.

CI does not require API keys, database credentials, or Ollama.

## Container publishing

The manual deployment workflow publishes the API image to GitHub Container Registry (GHCR). It accepts an image tag and also publishes the immutable commit SHA tag.

The workflow stops at image publication. The final hosting-provider deployment remains an explicit infrastructure action rather than assuming a cloud platform.

## Secrets boundary

No application secrets are committed. Runtime secrets such as database credentials and hosted-provider API keys must be supplied by the deployment environment. GitHub's GITHUB_TOKEN is used only for package publication.

## Deployment contract

A hosted environment must provide:

- PostgreSQL with pgvector.
- DATABASE_URL.
- An LLM provider endpoint.
- OLLAMA_BASE_URL when using Ollama.
- Provider model configuration.
- /health/readiness as the readiness check.

The V4.8 Compose credentials are development credentials and must not be reused for an internet-facing deployment.
