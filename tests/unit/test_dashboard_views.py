import unittest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestDashboardViews(unittest.TestCase):

    def test_admin_dashboard_view(self):
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Admin Dashboard", response.text)

    def test_supervisor_dashboard_view(self):
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Supervisor Dashboard", response.text)

    def test_dispatch_dashboard_view(self):
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Dispatcher Dashboard", response.text)

if __name__ == "__main__":
    unittest.main()