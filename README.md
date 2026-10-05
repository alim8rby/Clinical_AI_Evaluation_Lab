# Clinical AI Evaluation Lab (CAIEL)

CAIEL is an engineering platform for **building, evaluating, tracing, and investigating AI systems that answer clinical questions**.

It is deliberately more than a medical chatbot. The core workflow is:

**Question → Retrieval → Evidence → AI Answer → Evaluation → Failure Analysis → Experiment Comparison → Research Report**

The current demonstration domain is **depression**, using a controlled benchmark and evidence corpus. The project is designed as a portfolio/research system, **not for patient care or autonomous clinical decision-making**.

## What the project demonstrates

- Evidence-grounded RAG with citations and provenance
- Local LLM and embedding execution through Ollama
- Structured evaluation of retrieval, answer quality, grounding, and reliability
- Reproducible experiment configuration and immutable configuration hashes
- Failure classification, severity analysis, and regression signals
- Per-run evidence tracing from answer → claim → citation → chunk → document
- Experiment comparison and deterministic research reports
- FastAPI backend, PostgreSQL + pgvector persistence, and a browser UI
- Docker-based local deployment

## Current status

**V5 — Evaluation Platform: FROZEN**

V5.1–V5.12 are engineering complete. The final audit freezes the evaluation architecture and documents reproducibility, operational boundaries, and non-production security constraints.

The project does **not** claim:

- clinical validation
- clinical superiority
- production security
- bit-for-bit reproducibility of external model output
- autonomous clinical decision-making

## Architecture

```text
User Question
     ↓
Query / Retrieval
     ↓
Evidence Set
     ↓
Local LLM
     ↓
Structured Answer + Citations
     ↓
Evaluation
     ↓
Failure Analysis
     ↓
Experiment Comparison
     ↓
Research Report
```

## Tech stack

- Python
- FastAPI
- PostgreSQL
- pgvector
- Ollama
- Docker / Docker Compose
- HTML / CSS / JavaScript
- GitHub Actions

Default local models:

- Generation: `llama3.2:3b`
- Embeddings: `nomic-embed-text`

## Run CAIEL locally

This is the recommended way to try the project on Windows.

### 1. Prerequisites

Install and start:

- Docker Desktop
- Ollama
- Git
- VS Code

Then open a PowerShell terminal.

### 2. Get the repository

If you have not cloned it yet:

```powershell
git clone https://github.com/alim8rby/Clinical_AI_Evaluation_Lab.git
cd Clinical_AI_Evaluation_Lab
```

If you already have the repository:

```powershell
cd path\to\Clinical_AI_Evaluation_Lab
```

### 3. Check Ollama

Run:

```powershell
ollama --version
ollama list
```

Make sure these models are available:

```text
llama3.2:3b
nomic-embed-text
```

If they are missing:

```powershell
ollama pull llama3.2:3b
ollama pull nomic-embed-text
```

Leave Ollama running.

### 4. Start CAIEL

From the repository root:

```powershell
docker compose up --build
```

The first run may take several minutes because Docker needs to build the application image and download PostgreSQL/pgvector.

Wait until the API reports that it is running.

### 5. Open the application

Open:

**http://localhost:8000**

You should see the CAIEL dashboard.

You can also open the FastAPI API documentation at:

**http://localhost:8000/docs**

### 6. First test: ask a question

In the CAIEL interface:

1. Open **Clinical QA**.
2. Enter:

```text
What are common symptoms of depression?
```

3. Leave **Top K** at 5.
4. Click **Run QA**.

This exercises the retrieval + generation path.

### 7. Create your first experiment

Open **Experiments**.

Use the default values:

- Name: `Local Ollama baseline`
- Prompt version: `v1`
- Benchmark: `ClinicalQA-v1`
- Top K: `5`

Click **Create experiment**.

The experiment receives an immutable reproducibility configuration containing the model, embedding, retriever, evaluator, benchmark, prompt, and runtime versions.

### 8. Run a benchmark question

In the same Experiments screen:

- Question ID: `cq-001`
- Difficulty: `easy`
- Question:

```text
What are common symptoms of depression?
```

- Expected evidence ID:

```text
chunk_8cdc3807234ba4f0c
```

- Reference answer:

```text
Depression commonly involves persistent low mood or loss of interest, with associated cognitive, emotional, and physical symptoms.
```

- Key concepts:

```text
low mood,loss of interest
```

Click **Run question**.

### 9. Inspect what happened

After a run, the most useful parts of the platform are:

**Evidence Explorer**

Follow:

```text
Question
  → Answer
  → Claims
  → Citations
  → Retrieved chunks
  → Source documents
```

It also distinguishes evidence that was retrieved from evidence actually used in citations.

**Failure Observatory**

Inspect:

- failure categories
- failure types
- severity
- experiment-level failure rates
- baseline vs candidate regression signals

**Experiment Library**

Inspect:

- experiment configuration
- reproducibility hash
- model / embedding / retriever versions
- aggregate metrics
- completed runs

**Research Report**

Open the experiment's Markdown research report to see a durable summary of:

- experiment identity
- configuration provenance
- aggregate metrics
- recorded failures
- methodology
- limitations

## Useful API endpoints

Once the application is running:

| Purpose | Endpoint |
|---|---|
| Health | `GET /api/v1/health` |
| Readiness | `GET /health/readiness` |
| Ask a question | `POST /api/v1/qa` |
| List experiments | `GET /api/v1/experiments` |
| Get an experiment | `GET /api/v1/experiments/{id}` |
| Run a benchmark question | `POST /api/v1/experiments/{id}/runs` |
| Inspect a run | `GET /api/v1/runs/{id}` |
| Inspect run evidence | `GET /api/v1/runs/{id}/evidence/explorer` |
| Failure analysis | `GET /api/v1/failures/experiments/{id}/analysis` |
| Compare experiments | `POST /api/v1/comparisons` |
| Research report | `GET /api/v1/experiments/{id}/report/markdown` |

Interactive API documentation is available at:

**http://localhost:8000/docs**

## Stopping and restarting

To stop CAIEL:

```powershell
docker compose down
```

To start it again:

```powershell
docker compose up
```

Your PostgreSQL data is stored in the Docker volume `caiel_postgres`.

To remove the database volume as well:

```powershell
docker compose down -v
```

**Warning:** this deletes the local CAIEL PostgreSQL data.

## Troubleshooting

### Docker cannot connect to Ollama

CAIEL uses:

```text
http://host.docker.internal:11434
```

The Docker configuration is already set up for Windows Docker Desktop.

First make sure Ollama is running and the models exist:

```powershell
ollama list
```

Then restart CAIEL:

```powershell
docker compose down
docker compose up --build
```

### The API does not start

Check the container logs:

```powershell
docker compose logs api
```

For database problems:

```powershell
docker compose logs db
```

### Check container status

```powershell
docker compose ps
```

The database and API should eventually report healthy/running status.

## Testing

The repository contains focused unit tests and deterministic evaluation tests.

For a local development environment with Python installed:

```powershell
python -m unittest discover -s tests -v
```

The Docker walkthrough above is the recommended **first-time product test**. You do not need to run the test suite just to explore the application.

GitHub Actions is included for CI, but CI results are not treated as proof of runtime correctness for this portfolio project because the repository has an established GitHub environment issue.

## Project evolution

The project evolved through five major stages:

1. **V1 — RAG:** build an evidence-grounded clinical QA system.
2. **V2 — Evaluation:** measure retrieval, answers, grounding, and reliability.
3. **V3 — Failure Observatory:** understand why systems fail.
4. **V4 — Productionization:** add API, database, observability, Docker, and local runtime infrastructure.
5. **V5 — Evaluation Platform:** add calibration, benchmark v2, retrieval/generation research, experiment execution, statistics, failure analysis 2.0, evidence tracing, reproducibility, UX, research reports, and final audit/freeze.

## Repository documentation

- `docs/product-spec.md` — product definition
- `docs/roadmap.md` — overall roadmap and status
- `docs/roadmap-v5.md` — V5 evaluation-platform roadmap
- `docs/architecture/` — architecture and contracts
- `docs/methodology/` — evaluation methodology and audit records
- `docs/methodology/v5.12-audit.md` — final V5 audit and freeze

## Portfolio positioning

The strongest way to describe CAIEL is:

> **A platform for systematically evaluating, tracing, comparing, and investigating AI systems instead of simply trusting their outputs.**

Healthcare is the demonstration domain. The engineering principles are broader: retrieval quality, grounding, reliability, failure analysis, reproducibility, and experiment-driven AI development.

## License

MIT License. See [LICENSE](LICENSE).

## Disclaimer

CAIEL is a portfolio/research engineering project. It is not a medical device, clinical decision-support system, or substitute for professional medical judgment. Do not use it for patient care.
