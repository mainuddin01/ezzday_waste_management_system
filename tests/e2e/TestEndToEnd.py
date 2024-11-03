import unittest
from starlette.testclient import TestClient
from main import app
from components.auth.models import User

class TestEndToEnd(unittest.TestCase):

    def setUp(self):
        """Set up the TestClient and environment for E2E testing."""
        self.client = TestClient(app)

        # Create an admin user for testing
        self.admin_data = {
            'username': 'adminuser',
            'password': 'AdminPass123!',
            'role': 'Admin'
        }
        User(**self.admin_data).save()

        # Authenticate the user to get a session
        response = self.client.post("/auth/login", data={
            'username': self.admin_data['username'],
            'password': self.admin_data['password']
        })
        self.assertEqual(response.status_code, 303, "User should be able to log in.")
        self.cookies = response.cookies

    def tearDown(self):
        """Clean up after tests."""
        user = User.find_by_username(self.admin_data['username'])
        if user:
            user.delete()

    def test_e2e_workflow(self):
        """Test an end-to-end workflow from login to client creation, assignment, and report generation."""
        # Create a client
        response = self.client.post("/clients/add", data={
            'name': 'TestClientE2E',
            'client_type': 'Contractor',
            'description': 'E2E client test'
        }, cookies=self.cookies)
        self.assertEqual(response.status_code, 303, "Client should be successfully created.")

        # Create a zone
        response = self.client.post("/zones/add", data={
            'name': 'E2E Zone',
            'client_id': 1,
            'description': 'Zone for E2E test'
        }, cookies=self.cookies)
        self.assertEqual(response.status_code, 303, "Zone should be successfully created.")

        # Create a route within the zone
        response = self.client.post("/zones/1/routes/add", data={
            'name': 'E2E Route',
            'description': 'Route for E2E test'
        }, cookies=self.cookies)
        self.assertEqual(response.status_code, 303, "Route should be successfully created.")

        # Create an assignment for a crew
        response = self.client.post("/assignments/add", data={
            'crew_id': 1,
            'route_id': 1,
            'client_id': 1,
            'zone_id': 1,
            'assignment_date': '2024-12-01'
        }, cookies=self.cookies)
        self.assertEqual(response.status_code, 303, "Assignment should be successfully created.")

        # Generate a report
        response = self.client.post("/reports/generate", data={
            'report_type': 'End of Day'
        }, cookies=self.cookies)
        self.assertEqual(response.status_code, 200, "Report should be generated successfully.")

if __name__ == "__main__":
    unittest.main()