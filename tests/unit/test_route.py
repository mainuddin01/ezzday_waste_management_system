import unittest
from components.route.models import Route
from components.zone.models import Zone
from components.client.models import Client

class TestRoute(unittest.TestCase):

    def setUp(self):
        """Set up environment for testing routes."""
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

        self.route_data = {
            'name': 'Route 1',
            'zone_id': self.zone.id,
            'description': 'Route description for testing.'
        }

    def tearDown(self):
        """Clean up after each test."""
        routes = Route.find_all_by_zone_id(self.zone.id)
        for route in routes:
            route.delete()

        zones = Zone.find_all()
        for zone in zones:
            zone.delete()

        clients = Client.find_all()
        for client in clients:
            client.delete()

    def test_create_route_success(self):
        """Test creating a route successfully."""
        route = Route(**self.route_data)
        route.save()
        saved_route = Route.find_by_id(route.id)

        self.assertIsNotNone(saved_route, "Route should be successfully created.")
        self.assertEqual(saved_route.name, self.route_data['name'], "Route name should match.")

    def test_update_route(self):
        """Test updating a route."""
        route = Route(**self.route_data)
        route.save()

        updated_name = "Updated Route Name"
        route.name = updated_name
        route.save()

        updated_route = Route.find_by_id(route.id)
        self.assertEqual(updated_route.name, updated_name, "Route name should be updated.")

    def test_delete_route(self):
        """Test deleting a route."""
        route = Route(**self.route_data)
        route.save()

        route.delete()
        deleted_route = Route.find_by_id(route.id)

        self.assertIsNone(deleted_route, "Route should be deleted successfully.")

if __name__ == "__main__":
    unittest.main()