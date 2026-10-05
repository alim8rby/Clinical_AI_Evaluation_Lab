# Clinical AI Evaluation Lab (CAIEL)

**CAIEL is an engineering platform for evaluating, tracing, comparing, and investigating AI systems that answer clinical questions.**

It is deliberately more than a medical chatbot:

**Question → Retrieval → Evidence → AI Answer → Evaluation → Failure Analysis → Experiment Comparison → Research Report**

Healthcare is the demonstration domain; the engineering approach is broader.

> **Status: V5 Evaluation Platform — FROZEN**

CAIEL is a portfolio/research project, **not a clinical system and not for patient care**.

## What it demonstrates

- Evidence-grounded RAG with citations and provenance
- Local LLM + embedding execution through Ollama
- Retrieval, answer, grounding, and reliability evaluation
- Reproducible experiment configuration and immutable hashes
- Deterministic failure classification and regression analysis
- Per-run evidence tracing: answer → claim → citation → chunk → document
- Experiment comparison and research reports
- FastAPI + PostgreSQL/pgvector + Docker
- Browser-based workflow for running and inspecting experiments

## Architecture

```text
User Question
     ↓
Retrieval
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

**Python · FastAPI · PostgreSQL · pgvector · Ollama · Docker Compose · HTML/CSS/JavaScript · GitHub Actions**

Default local models:

- Generation: `llama3.2:3b`
- Embeddings: `nomic-embed-text`

## 5-minute local demo

### Prerequisites

Install:

- Docker Desktop
- Ollama
- Git
- VS Code

Make sure Ollama has the default models:

```powershell
ollama pull llama3.2:3b
ollama pull nomic-embed-text
```

### Start

```powershell
git clone https://github.com/alim8rby/Clinical_AI_Evaluation_Lab.git
cd Clinical_AI_Evaluation_Lab
docker compose up --build
```

Open:

- **CAIEL:** http://localhost:8000
- **API docs:** http://localhost:8000/docs

### Try the workflow

1. Open **Clinical QA** and ask:
   ```text
   What are common symptoms of depression?
   ```
2. Open **Experiments**.
3. Create a baseline experiment using:
   - Prompt: `v1`
   - Benchmark: `ClinicalQA-v1`
   - Top K: `5`
4. Run benchmark question **cq-001**.
5. Inspect the completed run in:
   - **Evidence Explorer** — trace answer → claim → citation → evidence → document
   - **Failure Observatory** — inspect classified failure signals
   - **Research Report** — inspect reproducibility, metrics, failures, and limitations

For `ClinicalQA-v1`, `cq-001` is:

```text
What clinical features are central to diagnosing a depressive episode?
```

## What makes the project different

A typical RAG demo asks:

> **“Can the model answer the question?”**

CAIEL asks:

> **“How well did the system retrieve evidence, generate the answer, ground its claims, handle reliability, and what exactly failed?”**

That distinction is the core of the project.

## Useful API endpoints

| Purpose | Endpoint |
|---|---|
| Health | `GET /api/v1/health` |
| Readiness | `GET /health/readiness` |
| Ask a question | `POST /api/v1/qa` |
| List experiments | `GET /api/v1/experiments` |
| Run benchmark question | `POST /api/v1/experiments/{id}/runs` |
| Inspect run | `GET /api/v1/runs/{id}` |
| Evidence Explorer | `GET /api/v1/runs/{id}/evidence/explorer` |
| Failure analysis | `GET /api/v1/failures/experiments/{id}/analysis` |
| Compare experiments | `POST /api/v1/comparisons` |
| Research report | `GET /api/v1/experiments/{id}/report/markdown` |

## V1 → V5 evolution

1. **V1 — RAG:** evidence-grounded clinical QA.
2. **V2 — Evaluation:** retrieval, answer, grounding, reliability metrics.
3. **V3 — Failure Observatory:** failure classification and investigation.
4. **V4 — Platform infrastructure:** API, database, observability, Docker, local runtime.
5. **V5 — Evaluation Platform:** calibration, benchmark v2, retrieval/generation research, experiment engine, statistics, failure analysis 2.0, evidence tracing, reproducibility, UX, research reports, and final audit/freeze.

## Engineering boundaries

CAIEL does **not** claim:

- clinical validation
- clinical superiority
- production security
- autonomous clinical decision-making
- bit-for-bit reproducibility of external model output

The benchmark and evidence corpus are compact engineering datasets, and model-assisted evaluation is not human clinical ground truth.

## Documentation

- `docs/portfolio-demo.md` — 5-minute portfolio demo script
- `docs/product-spec.md` — product definition
- `docs/roadmap.md` — overall roadmap
- `docs/roadmap-v5.md` — V5 roadmap and freeze
- `docs/architecture/` — architecture, boundaries, and decisions
- `docs/methodology/` — evaluation methodology and phase audits
- `docs/methodology/v5.12-audit.md` — final V5 audit

### Project status

**V5 is frozen.** The current repository is a portfolio/research evaluation platform. New work should be treated as V6 scope rather than incremental V5 feature growth.

The local demo is intentionally self-contained around Docker Compose + Ollama and uses a compact controlled benchmark/corpus. It is not a hosted production clinical service.

## Troubleshooting

Docker connects to local Ollama through:

```text
http://host.docker.internal:11434
```

Useful commands:

```powershell
docker compose ps
docker compose logs api
docker compose logs db
docker compose down
```

For local unit tests:

```powershell
python -m unittest discover -s tests -v
```

GitHub Actions is included for CI, but this project does not treat its current CI environment as proof of runtime correctness.

## Portfolio positioning

> **A platform for systematically evaluating, tracing, comparing, and investigating AI systems instead of simply trusting their outputs.**

## License

MIT License — see [LICENSE](LICENSE).

## Disclaimer

CAIEL is a portfolio/research engineering project. It is not a medical device, clinical decision-support system, or substitute for professional medical judgment. Do not use it for patient care.
