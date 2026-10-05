"""Initialize the CAIEL PostgreSQL schema for local/container deployment."""
from pathlib import Path

from sqlalchemy import create_engine, text

from app.backend.database import DATABASE_URL


MIGRATIONS = (
    ("001_initial", Path(__file__).resolve().parents[1] / "app" / "backend" / "migrations" / "001_initial.sql"),
    ("002_pgvector", Path(__file__).resolve().parents[1] / "app" / "backend" / "migrations" / "002_pgvector.sql"),
    ("003_semantic_embeddings", Path(__file__).resolve().parents[1] / "app" / "backend" / "migrations" / "003_semantic_embeddings.sql"),
    ("004_retrieval_trace", Path(__file__).resolve().parents[1] / "app" / "backend" / "migrations" / "004_retrieval_trace.sql"),
)


def main() -> None:
    if not DATABASE_URL.startswith(("postgresql://", "postgresql+psycopg://")):
        print("Skipping PostgreSQL migrations for non-PostgreSQL DATABASE_URL.")
        return

    engine = create_engine(DATABASE_URL)
    with engine.begin() as connection:
        connection.execute(
            text(
                "CREATE TABLE IF NOT EXISTS schema_migrations "
                "(version VARCHAR(100) PRIMARY KEY, applied_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)"
            )
        )
        for version, migration in MIGRATIONS:
            applied = connection.execute(
                text("SELECT 1 FROM schema_migrations WHERE version = :version"),
                {"version": version},
            ).scalar()
            if applied:
                continue
            connection.execute(text(migration.read_text(encoding="utf-8")))
            connection.execute(
                text("INSERT INTO schema_migrations (version) VALUES (:version)"),
                {"version": version},
            )
    print("CAIEL database initialized.")


if __name__ == "__main__":
    main()
