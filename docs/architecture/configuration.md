# Configuration & Environment

## Purpose

V0.5 defines how CAIEL receives runtime configuration and secrets. The goal is predictable local execution and reproducible experiments without committing credentials or machine-specific values.

## Configuration layers

Configuration is divided into three layers:

### 1. Environment variables

Used for secrets and deployment-specific values.

Examples:
- LLM provider API keys
- Database connection URL
- Runtime environment
- Application port

Environment variables are represented in `.env.example` and actual secrets remain local or in the deployment platform's secret manager.

### 2. Version-controlled configuration

Non-secret, reproducibility-relevant defaults belong under `configs/`.

Examples:
- Default model identifier
- Default retriever settings
- Chunking parameters
- Evaluation defaults
- Logging level
- Benchmark version

These values must not contain credentials.

### 3. Experiment configuration

An experiment captures the configuration snapshot needed to reproduce a run.

Experiment configuration includes:
- Model/provider configuration
- Retriever configuration
- Prompt version
- Benchmark version

The experiment record is authoritative for reproducing an executed experiment; later changes to defaults must not silently change historical experiments.

## Environment variables

The initial V0 environment contract is:

| Variable | Required | Purpose |
|---|---|---|
| `APP_ENV` | No | Runtime environment such as `development`, `test`, or `production` |
| `APP_HOST` | No | Application bind host |
| `APP_PORT` | No | Application port |
| `LOG_LEVEL` | No | Application logging level |
| `OPENAI_API_KEY` | Provider-dependent | LLM provider credential |
| `DATABASE_URL` | Later phase | Database connection string |

Provider-specific credentials may be added when a provider is implemented, but the application must not hard-code them.

## Safe defaults

Recommended development defaults:

| Setting | Development default |
|---|---|
| `APP_ENV` | `development` |
| `APP_HOST` | `127.0.0.1` |
| `APP_PORT` | `8000` |
| `LOG_LEVEL` | `INFO` |

These defaults are not deployment requirements.

## Provider abstraction

The application configuration should identify a provider and model rather than coupling the system to one vendor.

Conceptually:

```text
LLM_PROVIDER=...
LLM_MODEL=...
EMBEDDING_PROVIDER=...
EMBEDDING_MODEL=...
```

The concrete provider variables will be introduced when the corresponding integrations are implemented.

## Configuration precedence

When the same setting is supplied through multiple layers:

```text
Experiment snapshot
        ↓
Explicit runtime configuration
        ↓
Version-controlled defaults
        ↓
Application safe defaults
```

Secrets are always resolved from the environment/secret manager and are never stored in experiment records.

## Reproducibility rules

1. No secret is committed to Git.
2. `.env.example` documents required environment variables without values.
3. Non-secret defaults are version controlled.
4. Experiment records preserve configuration snapshots relevant to a run.
5. Historical experiments do not depend on mutable global defaults.
6. Provider SDK credentials are accessed only through the provider abstraction.
7. Test configuration must be isolated from production configuration.

## Local development contract

A developer should be able to:

1. Copy `.env.example` to a local environment file.
2. Add required credentials.
3. Install the project dependencies.
4. Start the application using the documented runtime command.
5. Run tests using the documented test command.

Exact commands are implementation details and will be documented when the application is implemented.

## V0.5 scope boundary

V0.5 does not implement:
- Secret management infrastructure
- Cloud configuration
- Docker runtime configuration
- Database provisioning
- Provider integrations
- Configuration loading code
- Pydantic settings models
- Production deployment settings
