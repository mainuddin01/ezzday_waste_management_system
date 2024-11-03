import unittest
from components.driver.models import Driver
from components.loader.models import Loader

class TestDriverLoader(unittest.TestCase):

    def setUp(self):
        self.driver_data = {
            'name': 'John Driver',
            'license_expiry_date': '2025-01-01',
            'last_medical_check': '2023-01-01'
        }

        self.loader_data = {
            'name': 'Loader Mike',
            'pickup_spot': 'Zone A'
        }

    def test_create_driver(self):
        driver = Driver(**self.driver_data)
        driver.save()
        fetched_driver = Driver.find_by_id(driver.id)
        self.assertEqual(fetched_driver.name, self.driver_data['name'])

    def test_create_loader(self):
        loader = Loader(**self.loader_data)
        loader.save()
        fetched_loader = Loader.find_by_id(loader.id)
        self.assertEqual(fetched_loader.pickup_spot, self.loader_data['pickup_spot'])

if __name__ == "__main__":
    unittest.main()