import json
import tempfile
import unittest

from fastapi.testclient import TestClient

from app.backend.main import app
from app.backend.services import services
from src.failure_analysis.models import Failure, FailureSeverity
from src.failure_analysis.store import FailureStore


class ApiV41Tests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.tmp.close()
        services.observatory = __import__(
            "src.failure_analysis",
            fromlist=["FailureObservatory"],
        ).FailureObservatory(FailureStore(self.tmp.name))
        self.client = TestClient(app)

    def tearDown(self):
        import os
        services.rag = None
        os.unlink(self.tmp.name)

    def _failure(self):
        return Failure(
            failure_id="run-1:generation:hallucination",
            run_id="run-1",
            question_id="cq-1",
            category="GENERATION",
            type="Hallucination",
            severity=FailureSeverity.HIGH,
            description="Unsupported claim signal.",
            evidence="unsupported_claim_rate=0.75",
            metric="unsupported_claim_rate",
            metric_value=0.75,
            classifier_version="failure-v1",
        )

    def test_failure_list_and_summary(self):
        services.observatory.store.save(self._failure())
        response = self.client.get("/api/v1/failures")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["failures"][0]["failure_id"], "run-1:generation:hallucination")

        summary = self.client.get("/api/v1/failures/summary")
        self.assertEqual(summary.status_code, 200)
        self.assertEqual(summary.json()["total"], 1)
        self.assertEqual(summary.json()["by_category"], {"GENERATION": 1})

    def test_failure_detail_not_found(self):
        response = self.client.get("/api/v1/failures/missing")
        self.assertEqual(response.status_code, 404)

    def test_failure_filter_and_limit(self):
        services.observatory.store.save(self._failure())
        response = self.client.get("/api/v1/failures?severity=HIGH&limit=1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["failures"]), 1)

    def test_qa_reports_not_configured_without_faking_success(self):
        response = self.client.post("/api/v1/qa", json={"question": "What is depression?"})
        self.assertEqual(response.status_code, 503)


if __name__ == "__main__":
    unittest.main()
