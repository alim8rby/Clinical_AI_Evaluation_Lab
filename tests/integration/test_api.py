import unittest
from fastapi.testclient import TestClient
from app.backend.main import app

class ApiFoundationTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_health(self):
        response = self.client.get("/api/v1/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status":"ok","environment":"development","version":"0.4.0"})

    def test_not_found_error_contract(self):
        response = self.client.get("/api/v1/experiments/missing")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["error"], {"code":"NOT_FOUND","message":"experiment not found","details":{}})

if __name__ == "__main__":
    unittest.main()
