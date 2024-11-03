import unittest
from components.client.models import Client

class TestClient(unittest.TestCase):

    def setUp(self):
        self.client_data = {
            'name': 'Test Client',
            'client_type': 'Contractor',
            'description': 'Test description',
            'contact_name': 'John Doe',
            'contact_phone': '1234567890',
            'contact_email': 'john.doe@example.com'
        }

    def test_create_client(self):
        client = Client(**self.client_data)
        client.save()
        fetched_client = Client.find_by_id(client.id)
        self.assertEqual(fetched_client.name, self.client_data['name'])

    def test_delete_client(self):
        client = Client(**self.client_data)
        client.save()
        client.delete()
        deleted_client = Client.find_by_id(client.id)
        self.assertIsNone(deleted_client)

if __name__ == "__main__":
    unittest.main()