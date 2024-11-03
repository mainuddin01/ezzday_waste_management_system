import unittest
from components.assignment.models import Assignment
from components.crew.models import Crew
from components.route.models import Route
from components.zone.models import Zone
from components.client.models import Client

class TestAssignment(unittest.TestCase):

    def setUp(self):
        """Set up environment for testing assignments."""
        # Set up client, zone, route, and crew
        self.client = Client(
            name="TestClient",
            client_type="Contractor",
            description="A test client"
        )
        self.client.save()

        self.zone = Zone(
            name="TestZone",
            client_id=self.client.id,
            description="A test zone"
        )
        self.zone.save()

        self.route = Route(
            name="Route 1",
            zone_id=self.zone.id,
            description="A test route"
        )
        self.route.save()

        self.crew = Crew(
            driver_id=1,
            loader_ids=[1, 2],
            fleet_id=1,
            assignment_status="Ready"
        )
        self.crew.save()

        self.assignment_data = {
            'crew_id': self.crew.id,
            'route_id': self.route.id,
            'client_id': self.client.id,
            'zone_id': self.zone.id,
            'assignment_date': '2024-10-15'
        }

    def tearDown(self):
        """Clean up after each test."""
        assignments = Assignment.find_all_for_date('2024-10-15')
        for assignment in assignments:
            assignment.delete()

        crews = Crew.find_all()
        for crew in crews:
            crew.delete()

        routes = Route.find_all_by_zone_id(self.zone.id)
        for route in routes:
            route.delete()

        zones = Zone.find_all()
        for zone in zones:
            zone.delete()

        clients = Client.find_all()
        for client in clients:
            client.delete()

    def test_create_assignment_success(self):
        """Test creating an assignment."""
        assignment = Assignment(**self.assignment_data)
        assignment.save()
        saved_assignment = Assignment.find_by_id(assignment.id)

        self.assertIsNotNone(saved_assignment, "Assignment should be successfully created.")
        self.assertEqual(saved_assignment.crew_id, self.crew.id, "Crew ID should match.")

    def test_update_assignment_status(self):
        """Test updating the status of an assignment."""
        assignment = Assignment(**self.assignment_data)
        assignment.save()

        assignment.status_updates = {'11AM': 'On Track'}
        assignment.save()

        updated_assignment = Assignment.find_by_id(assignment.id)
        self.assertEqual(updated_assignment.status_updates['11AM'], 'On Track', "Status should be updated.")

    def test_delete_assignment(self):
        """Test deleting an assignment."""
        assignment = Assignment(**self.assignment_data)
        assignment.save()

        assignment.delete()
        deleted_assignment = Assignment.find_by_id(assignment.id)

        self.assertIsNone(deleted_assignment, "Assignment should be deleted successfully.")

if __name__ == "__main__":
    unittest.main()