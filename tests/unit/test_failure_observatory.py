import tempfile
import unittest
from pathlib import Path

from src.failure_analysis.models import Failure, FailureSeverity
from src.failure_analysis.observatory import (
    FailureNotFoundError,
    FailureObservatory,
    FailureQuery,
)
from src.failure_analysis.store import FailureStore


def make_failure(failure_id, category="GENERATION", severity=FailureSeverity.HIGH):
    return Failure(
        failure_id=failure_id,
        run_id="run-1",
        question_id="cq-001",
        category=category,
        type="Hallucination",
        severity=severity,
        description="Failure description.",
        evidence="Failure evidence.",
    )


class FailureObservatoryTests(unittest.TestCase):
    def make_observatory(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        store = FailureStore(Path(directory.name) / "failures.json")
        store.save_many([
            make_failure("f-2", "RETRIEVAL", FailureSeverity.MEDIUM),
            make_failure("f-1"),
            make_failure("f-3", "SAFETY", FailureSeverity.CRITICAL),
        ])
        return FailureObservatory(store)

    def test_list_is_deterministic(self):
        observatory = self.make_observatory()
        result = observatory.list_failures()
        self.assertEqual([item.failure_id for item in result], ["f-1", "f-2", "f-3"])

    def test_query_filters_and_limits(self):
        observatory = self.make_observatory()
        result = observatory.list_failures(
            FailureQuery(severity="HIGH", limit=1)
        )
        self.assertEqual([item.failure_id for item in result], ["f-1"])

    def test_get_missing_failure_raises(self):
        observatory = self.make_observatory()
        with self.assertRaises(FailureNotFoundError):
            observatory.get_failure("missing")

    def test_snapshot_contains_failures_and_summary(self):
        observatory = self.make_observatory()
        snapshot = observatory.snapshot(FailureQuery(category="SAFETY"))
        self.assertEqual([item.failure_id for item in snapshot.failures], ["f-3"])
        self.assertEqual(snapshot.summary.total, 1)
        self.assertEqual(snapshot.summary.by_category, {"SAFETY": 1})

    def test_query_rejects_non_positive_limit(self):
        with self.assertRaises(ValueError):
            FailureQuery(limit=0)
