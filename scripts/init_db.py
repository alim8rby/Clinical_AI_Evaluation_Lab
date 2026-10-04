"""Initialize the CAIEL PostgreSQL schema for local/container deployment."""
from pathlib import Path

from sqlalchemy import create_engine, text

from app.backend.database import DATABASE_URL


MIGRATIONS = (
    Path(__file__).resolve().parents[1] / "app" / "backend" / "migrations" / "001_initial.sql",
    Path(__file__).resolve().parents[1] / "app" / "backend" / "migrations" / "002_pgvector.sql",
)


def main() -> None:
    if not DATABASE_URL.startswith(("postgresql://", "postgresql+psycopg://")):
        print("Skipping PostgreSQL migrations for non-PostgreSQL DATABASE_URL.")
        return

    engine = create_engine(DATABASE_URL)
    with engine.begin() as connection:
        for migration in MIGRATIONS:
            connection.execute(text(migration.read_text(encoding="utf-8")))
    print("CAIEL database initialized.")


if __name__ == "__main__":
    main()
