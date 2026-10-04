import unittest
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.backend.database import Base
from app.backend.repositories import FailureRepository
from src.failure_analysis.models import Failure, FailureSeverity


class FailureRepositoryTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()

    def tearDown(self):
        self.session.close()
        self.engine.dispose()

    def failure(self, failure_id="f-1"):
        return Failure(
            failure_id=failure_id,
            run_id="run-1",
            question_id="cq-1",
            category="GENERATION",
            type="Hallucination",
            severity=FailureSeverity.HIGH,
            description="Unsupported claim.",
            evidence="unsupported_claim_rate=0.75",
            metric="unsupported_claim_rate",
            metric_value=0.75,
            created_at=datetime(2026, 10, 4, 12, 0),
        )

    def test_roundtrip_and_deterministic_list(self):
        repo = FailureRepository(self.session)
        repo.save(self.failure("f-2"))
        repo.save(self.failure("f-1"))
        self.assertEqual([f.failure_id for f in repo.list()], ["f-1", "f-2"])
        self.assertEqual(repo.get("f-1"), self.failure("f-1"))
        self.assertEqual(repo.count(), 2)

    def test_conflicting_id_is_rejected(self):
        repo = FailureRepository(self.session)
        repo.save(self.failure())
        conflicting = self.failure()
        object.__setattr__(conflicting, "evidence", "different")
        with self.assertRaises(ValueError):
            repo.save(conflicting)
