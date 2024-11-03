import unittest
from components.zone.models import Zone
from components.client.models import Client

class TestZone(unittest.TestCase):

    def setUp(self):
        """Set up environment for testing zones."""
        self.client = Client(
            name="TestClient",
            client_type="Contractor",
            description="A test client"
        )
        self.client.save()

        self.zone_data = {
            'name': 'Zone A',
            'client_id': self.client.id,
            'description': 'This is a test zone.'
        }

    def tearDown(self):
        """Clean up after each test."""
        zones = Zone.find_all()
        for zone in zones:
            zone.delete()

        clients = Client.find_all()
        for client in clients:
            client.delete()

    def test_create_zone_success(self):
        """Test creating a new zone."""
        zone = Zone(**self.zone_data)
        zone.save()
        saved_zone = Zone.find_by_id(zone.id)

        self.assertIsNotNone(saved_zone, "Zone should be successfully created.")
        self.assertEqual(saved_zone.name, self.zone_data['name'], "Zone name should match.")

    def test_update_zone(self):
        """Test updating an existing zone."""
        zone = Zone(**self.zone_data)
        zone.save()

        updated_description = "Updated zone description."
        zone.description = updated_description
        zone.save()

        updated_zone = Zone.find_by_id(zone.id)
        self.assertEqual(updated_zone.description, updated_description, "Zone description should be updated.")

    def test_delete_zone(self):
        """Test deleting an existing zone."""
        zone = Zone(**self.zone_data)
        zone.save()

        zone.delete()
        deleted_zone = Zone.find_by_id(zone.id)

        self.assertIsNone(deleted_zone, "Zone should be deleted successfully.")

if __name__ == "__main__":
    unittest.main()