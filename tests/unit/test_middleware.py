import unittest
from starlette.testclient import TestClient
from main import app

class TestMiddleware(unittest.TestCase):

    def setUp(self):
        """Set up environment for testing middleware."""
        self.client = TestClient(app)

    def test_session_middleware(self):
        """Test if session cookie is set properly."""
        response = self.client.get("/")
        self.assertIn("set-cookie", response.headers, "Session cookie should be set.")

    def test_cors_middleware(self):
        """Test if CORS headers are set properly."""
        response = self.client.options("/", headers={
            "origin": "http://localhost",
            "access-control-request-method": "GET"
        })
        self.assertEqual(response.headers.get("access-control-allow-origin"), "http://localhost", "CORS headers should be properly set.")

if __name__ == "__main__":
    unittest.main()