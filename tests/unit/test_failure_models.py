import unittest
from datetime import datetime, timezone

from src.failure_analysis.models import Failure, FailureSeverity, failure_from_dict


class FailureModelTests(unittest.TestCase):
    def test_valid_failure_serializes_deterministically(self):
        failure = Failure(
            failure_id="failure-1",
            run_id="run-1",
            question_id="cq-001",
            answer_id="answer-1",
            category="GENERATION",
            type="Hallucination",
            severity=FailureSeverity.HIGH,
            description="Claim is not supported.",
            evidence="The retrieved evidence does not support the claim.",
            metric="unsupported_claim_rate",
            metric_value=0.75,
            created_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        )
        payload = failure.to_dict()
        restored = failure_from_dict(payload)

        self.assertEqual(restored, failure)
        self.assertEqual(failure.to_json(), failure.to_json())
        self.assertEqual(payload["severity"], "HIGH")

    def test_empty_required_field_is_rejected(self):
        with self.assertRaises(ValueError):
            Failure(
                failure_id="",
                run_id="run-1",
                question_id="cq-001",
                category="GENERATION",
                type="Hallucination",
                severity=FailureSeverity.HIGH,
                description="bad",
                evidence="bad",
            )

    def test_invalid_severity_is_rejected(self):
        with self.assertRaises(ValueError):
            Failure(
                failure_id="failure-1",
                run_id="run-1",
                question_id="cq-001",
                category="GENERATION",
                type="Hallucination",
                severity="HIGH",
                description="bad",
                evidence="bad",
            )

    def test_missing_serialized_field_is_rejected(self):
        with self.assertRaises(ValueError):
            failure_from_dict({"failure_id": "failure-1"})
