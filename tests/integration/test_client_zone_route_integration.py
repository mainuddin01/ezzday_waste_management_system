import unittest
from components.client.models import Client
from components.zone.models import Zone
from components.route.models import Route

class TestClientZoneRouteIntegration(unittest.TestCase):

    def setUp(self):
        self.client_data = {
            'name': 'Test Client',
            'client_type': 'Contractor',
            'description': 'Test description',
            'contact_name': 'Jane Doe',
            'contact_phone': '1234567890',
            'contact_email': 'jane.doe@example.com'
        }
        self.zone_data = {
            'name': 'Zone A',
            'client_id': 1,
            'description': 'Residential Area'
        }
        self.route_data = {
            'name': 'Route 101',
            'zone_id': 1,
            'description': 'Morning Pickup'
        }

    def test_client_zone_route_integration(self):
        # Create Client
        client = Client(**self.client_data)
        client.save()

        # Create Zone linked to Client
        zone = Zone(**self.zone_data)
        zone.client_id = client.id
        zone.save()

        # Create Route linked to Zone
        route = Route(**self.route_data)
        route.zone_id = zone.id
        route.save()

        # Check if all are correctly linked
        fetched_client = Client.find_by_id(client.id)
        fetched_zone = Zone.find_by_id(zone.id)
        fetched_route = Route.find_by_id(route.id)
        
        self.assertEqual(fetched_zone.client_id, fetched_client.id)
        self.assertEqual(fetched_route.zone_id, fetched_zone.id)

if __name__ == "__main__":
    unittest.main()