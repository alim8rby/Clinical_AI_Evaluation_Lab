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

    def test_invalid_request_error_contract(self):
        @app.get("/api/v1/test-invalid-request")
        def invalid_request():
            raise ValueError("example validation error")
        response = self.client.get("/api/v1/test-invalid-request")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], {"code":"INVALID_REQUEST","message":"example validation error","details":{}})

if __name__ == "__main__":
    unittest.main()
