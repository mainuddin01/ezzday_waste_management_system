import unittest
from components.route.models import Route
from components.assignment.models import Assignment
from components.crew.models import Crew
from components.client.models import Client
from components.zone.models import Zone

class TestRouteAssignmentIntegration(unittest.TestCase):

    def setUp(self):
        """Set up environment for testing route and assignment integration."""
        # Set up client, zone, route, and crew
        self.client = Client(name="IntegrationClient", client_type="Contractor")
        self.client.save()

        self.zone = Zone(name="IntegrationZone", client_id=self.client.id)
        self.zone.save()

        self.route = Route(name="IntegrationRoute", zone_id=self.zone.id)
        self.route.save()

        self.crew = Crew(driver_id=1, loader_ids=[1, 2], fleet_id=1)
        self.crew.save()

    def tearDown(self):
        """Clean up after each test."""
        Assignment.find_all()
        self.crew.delete()
        self.route.delete()
        self.zone.delete()
        self.client.delete()

    def test_assign_route_to_crew(self):
        """Test assigning a route to a crew and ensure everything connects correctly."""
        assignment = Assignment(
            crew_id=self.crew.id,
            route_id=self.route.id,
            client_id=self.client.id,
            zone_id=self.zone.id,
            assignment_date="2024-10-20"
        )
        assignment.save()

        # Validate assignment relationship
        self.assertEqual(assignment.crew_id, self.crew.id, "Crew should be assigned to the route correctly.")
        self.assertEqual(assignment.route_id, self.route.id, "Route should be linked to assignment correctly.")

if __name__ == "__main__":
    unittest.main()