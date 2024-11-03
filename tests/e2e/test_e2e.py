import unittest
import json
from starlette.testclient import TestClient
from fasthtml import FastHTML
from routes import setup_routes
from settings import SECRET_KEY

# Setting up the app for testing
app = FastHTML()
setup_routes(app)
client = TestClient(app)

class TestE2E(unittest.TestCase):
    
    def setUp(self):
        """Set up environment before each test case."""
        self.client = client

        # Common headers for requests
        self.headers = {
            "Content-Type": "application/json"
        }

        # Sample Data
        self.valid_user_data = {
            "username": "e2e_test_user",
            "password": "e2e_TestPassword123!",
            "role": "Admin"
        }

        # Register a test user
        response = self.client.post("/auth/register", data=json.dumps(self.valid_user_data), headers=self.headers)
        self.assertEqual(response.status_code, 201, "Failed to set up the test user.")

        # Log in with the test user
        response = self.client.post("/auth/login", data=json.dumps({
            "username": self.valid_user_data["username"],
            "password": self.valid_user_data["password"]
        }), headers=self.headers)
        self.assertEqual(response.status_code, 200, "Failed to log in the test user.")
        self.auth_token = response.json()["token"]

    def tearDown(self):
        """Clean up after each test method."""
        response = self.client.delete(f"/clients/delete/{self.client_id}", headers=self.get_auth_headers())
        self.assertTrue(response.status_code in [200, 404])

    def get_auth_headers(self):
        """Helper function to get headers with authentication token."""
        return {**self.headers, "Authorization": f"Bearer {self.auth_token}"}

    def test_end_to_end_workflow(self):
        """Test the complete end-to-end workflow for the waste management system."""
        
        # 1. Add a new client
        client_data = {
            "name": "Test Client",
            "client_type": "Contractor",
            "description": "A client for testing",
            "contact_name": "John Doe",
            "contact_phone": "1234567890",
            "contact_email": "testclient@example.com",
            "zones_serviced": ["Zone A"]
        }
        response = self.client.post("/clients/add", data=json.dumps(client_data), headers=self.get_auth_headers())
        self.assertEqual(response.status_code, 201, "Failed to add client")
        self.client_id = response.json().get("id")

        # 2. Add a new zone
        zone_data = {
            "name": "Zone A",
            "client_id": self.client_id,
            "description": "Test zone"
        }
        response = self.client.post("/zones/add", data=json.dumps(zone_data), headers=self.get_auth_headers())
        self.assertEqual(response.status_code, 201, "Failed to add zone")
        zone_id = response.json().get("id")

        # 3. Add a route to the zone
        route_data = {
            "name": "Route 1",
            "zone_id": zone_id,
            "description": "Route for Zone A"
        }
        response = self.client.post(f"/zones/{zone_id}/routes/add", data=json.dumps(route_data), headers=self.get_auth_headers())
        self.assertEqual(response.status_code, 201, "Failed to add route")
        route_id = response.json().get("id")

        # 4. Add a driver and loader
        driver_data = {
            "name": "Test Driver",
            "license_expiry_date": "2025-10-12",
            "last_medical_check": "2023-10-12"
        }
        response = self.client.post("/drivers/add", data=json.dumps(driver_data), headers=self.get_auth_headers())
        self.assertEqual(response.status_code, 201, "Failed to add driver")
        driver_id = response.json().get("id")

        loader_data = {
            "name": "Test Loader",
            "pickup_spot": "Zone A - Spot 1"
        }
        response = self.client.post("/loaders/add", data=json.dumps(loader_data), headers=self.get_auth_headers())
        self.assertEqual(response.status_code, 201, "Failed to add loader")
        loader_id = response.json().get("id")

        # 5. Add a truck
        truck_data = {
            "truck_number": "T101",
            "plate_number": "TEST-101",
            "truck_type": "Heavy-duty Garbage Truck",
            "capacity": 5000
        }
        response = self.client.post("/fleet/add", data=json.dumps(truck_data), headers=self.get_auth_headers())
        self.assertEqual(response.status_code, 201, "Failed to add truck")
        truck_id = response.json().get("id")

        # 6. Create a crew with the driver and loader
        crew_data = {
            "driver_id": driver_id,
            "loader_ids": [loader_id],
            "truck_id": truck_id
        }
        response = self.client.post("/crews/add", data=json.dumps(crew_data), headers=self.get_auth_headers())
        self.assertEqual(response.status_code, 201, "Failed to create crew")
        crew_id = response.json().get("id")

        # 7. Assign the crew to the route
        assignment_data = {
            "crew_id": crew_id,
            "route_id": route_id,
            "client_id": self.client_id,
            "assignment_date": "2024-10-12"
        }
        response = self.client.post("/assignments/add", data=json.dumps(assignment_data), headers=self.get_auth_headers())
        self.assertEqual(response.status_code, 201, "Failed to create assignment")
        assignment_id = response.json().get("id")

        # 8. Generate schedule
        response = self.client.post("/schedules/generate", data=json.dumps({"week_number": 41}), headers=self.get_auth_headers())
        self.assertEqual(response.status_code, 201, "Failed to generate schedule")

        # 9. Generate a report for the day's assignment
        report_data = {
            "report_type": "End of Day",
            "parameters": {"assignment_id": assignment_id}
        }
        response = self.client.post("/reports/generate", data=json.dumps(report_data), headers=self.get_auth_headers())
        self.assertEqual(response.status_code, 201, "Failed to generate report")

        # 10. Mark attendance and update assignment status
        response = self.client.post(f"/assignments/attendance", data=json.dumps({"assignment_id": assignment_id, "status": "Confirmed"}), headers=self.get_auth_headers())
        self.assertEqual(response.status_code, 200, "Failed to mark attendance")

        status_update_data = {
            "assignment_id": assignment_id,
            "status_update": {
                "time_label": "11AM",
                "status": "On Route"
            }
        }
        response = self.client.post(f"/assignments/status/update/11AM", data=json.dumps(status_update_data), headers=self.get_auth_headers())
        self.assertEqual(response.status_code, 200, "Failed to update assignment status")

        # 11. View generated reports
        response = self.client.get("/reports", headers=self.get_auth_headers())
        self.assertEqual(response.status_code, 200, "Failed to view reports")

        # 12. Clean up - delete client and its associated data
        response = self.client.delete(f"/clients/delete/{self.client_id}", headers=self.get_auth_headers())
        self.assertEqual(response.status_code, 200, "Failed to delete client")

    @classmethod
    def tearDownClass(cls):
        """Clean up any shared resources after all tests have run."""
        # Cleanup logic for the entire class if needed
        pass

if __name__ == "__main__":
    unittest.main()