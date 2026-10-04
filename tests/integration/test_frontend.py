import unittest
from fastapi.testclient import TestClient

from app.backend.main import app


class FrontendIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_root_serves_frontend(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Clinical AI Evaluation Lab", response.text)
        self.assertIn("/app.js", response.text)

    def test_frontend_assets_are_served(self):
        response = self.client.get("/app.js")
        self.assertEqual(response.status_code, 200)
        self.assertIn("/api/v1", response.text)

        response = self.client.get("/styles.css")
        self.assertEqual(response.status_code, 200)
        self.assertIn(".shell", response.text)


if __name__ == "__main__":
    unittest.main()
