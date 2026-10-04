import unittest
from fastapi.testclient import TestClient
from app.backend.main import app
from app.backend.services import services
from src.failure_analysis import FailureObservatory
from src.failure_analysis.store import FailureStore
import tempfile

class ApiFoundationTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.tmp.close()
        services.observatory = FailureObservatory(FailureStore(self.tmp.name))

    def tearDown(self):
        import os
        os.unlink(self.tmp.name)

    def test_health(self):
        response = self.client.get("/api/v1/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status":"ok","environment":"development","version":"0.4.0"})

    def test_not_found_error_contract(self):
        response = self.client.get("/api/v1/failures/missing")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["error"], {"code":"NOT_FOUND","message":"failure not found","details":{}})

if __name__ == "__main__":
    unittest.main()
