import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from src.failure_analysis.models import Failure, FailureSeverity
from src.failure_analysis.store import (
    FailureAlreadyExistsError,
    FailureStore,
    FailureStoreError,
)


def make_failure(failure_id: str) -> Failure:
    return Failure(
        failure_id=failure_id,
        run_id="run-1",
        question_id="cq-001",
        answer_id="answer-1",
        category="GENERATION",
        type="Hallucination",
        severity=FailureSeverity.HIGH,
        description="Claim is not supported.",
        evidence="Retrieved evidence does not support the claim.",
        metric="unsupported_claim_rate",
        metric_value=0.75,
        created_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
    )


class FailureStoreTests(unittest.TestCase):
    def test_save_and_load_round_trip(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "failures.json"
            store = FailureStore(path)
            failure = make_failure("failure-2")

            store.save(failure)

            restored = FailureStore(path).get("failure-2")
            self.assertEqual(restored, failure)
            self.assertEqual(store.count(), 1)

    def test_missing_store_is_empty(self):
        with tempfile.TemporaryDirectory() as directory:
            store = FailureStore(Path(directory) / "missing.json")
            self.assertEqual(store.list(), [])
            self.assertEqual(store.count(), 0)

    def test_records_are_sorted_deterministically(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "failures.json"
            store = FailureStore(path)

            store.save_many([make_failure("failure-2"), make_failure("failure-1")])

            self.assertEqual(
                [failure.failure_id for failure in store.list()],
                ["failure-1", "failure-2"],
            )
            payload = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(
                [record["failure_id"] for record in payload],
                ["failure-1", "failure-2"],
            )

    def test_same_failure_id_is_idempotent(self):
        with tempfile.TemporaryDirectory() as directory:
            store = FailureStore(Path(directory) / "failures.json")
            failure = make_failure("failure-1")

            store.save(failure)
            store.save(failure)

            self.assertEqual(store.count(), 1)

    def test_conflicting_failure_id_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            store = FailureStore(Path(directory) / "failures.json")
            store.save(make_failure("failure-1"))

            original = make_failure("failure-1")
            conflicting = Failure(
                failure_id=original.failure_id,
                run_id=original.run_id,
                question_id=original.question_id,
                answer_id=original.answer_id,
                category=original.category,
                type=original.type,
                severity=original.severity,
                description="Different content.",
                evidence=original.evidence,
                metric=original.metric,
                metric_value=original.metric_value,
                classifier_version=original.classifier_version,
                created_at=original.created_at,
            )

            with self.assertRaises(FailureAlreadyExistsError):
                store.save(conflicting)

    def test_invalid_json_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "failures.json"
            path.write_text("{invalid", encoding="utf-8")

            with self.assertRaises(FailureStoreError):
                FailureStore(path).list()

    def test_non_list_root_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "failures.json"
            path.write_text('{"failure_id": "failure-1"}', encoding="utf-8")

            with self.assertRaises(FailureStoreError):
                FailureStore(path).list()
