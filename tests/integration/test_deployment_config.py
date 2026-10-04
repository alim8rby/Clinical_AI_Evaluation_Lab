import unittest
from pathlib import Path


class DeploymentConfigTests(unittest.TestCase):
    ROOT = Path(__file__).resolve().parents[2]

    def test_dockerfile_exists(self):
        content = (self.ROOT / "Dockerfile").read_text(encoding="utf-8")
        self.assertIn("uvicorn app.backend.main:app", content)

    def test_compose_has_postgres_and_api_healthcheck(self):
        content = (self.ROOT / "docker-compose.yml").read_text(encoding="utf-8")
        self.assertIn("pgvector/pgvector:pg16", content)
        self.assertIn("DATABASE_URL: postgresql+psycopg://caiel:caiel@db:5432/caiel", content)
        self.assertIn("healthcheck:", content)
        self.assertIn("host.docker.internal:host-gateway", content)

    def test_database_initializer_is_idempotent(self):
        content = (self.ROOT / "scripts" / "init_db.py").read_text(encoding="utf-8")
        self.assertIn("schema_migrations", content)
        self.assertIn("WHERE version = :version", content)


if __name__ == "__main__":
    unittest.main()
