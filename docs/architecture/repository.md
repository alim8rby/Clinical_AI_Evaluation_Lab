# Repository Architecture

The repository separates application code, domain modules, data, tests, configuration, documentation, and operational scripts.

| Directory | Responsibility |
|---|---|
| `app/` | Application entry points and user-facing interfaces |
| `src/ingestion/` | Document ingestion |
| `src/preprocessing/` | Parsing, cleaning, chunking, metadata |
| `src/retrieval/` | Retrieval strategies and evidence selection |
| `src/generation/` | Model abstraction and answer generation |
| `src/evaluation/` | Evaluation metrics and scoring |
| `src/experiments/` | Reproducible experiment orchestration |
| `src/failure_analysis/` | Failure classification and analysis |
| `src/monitoring/` | Runtime and operational observability |
| `data/` | Raw, processed, benchmark, and result data |
| `tests/` | Unit, integration, retrieval, and evaluation tests |
| `configs/` | Non-secret configuration |
| `docs/` | Architecture, methodology, experiments, and safety documentation |
| `scripts/` | Small operational or development utilities |

## Boundary rule

A directory should contain only artifacts belonging to its stated responsibility. New architectural components require an explicit decision rather than being added opportunistically.
