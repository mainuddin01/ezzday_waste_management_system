import unittest
from components.crew.service import create_crew, get_crew_by_id, delete_crew
from components.fleet.service import create_truck, delete_truck
from components.driver.service import create_driver, delete_driver
from components.loader.service import create_loader, delete_loader

class TestCrewAndFleetService(unittest.TestCase):

    def setUp(self):
        # Set up the necessary components
        self.truck_data = {
            'truck_number': 'T101',
            'plate_number': 'TEST-101',
            'truck_type': 'Heavy-duty Garbage Truck',
            'capacity': 5000
        }
        self.driver_data = {
            'name': 'Driver John',
            'license_expiry_date': '2025-10-12',
            'last_medical_check': '2023-10-12'
        }
        self.loader_data = {
            'name': 'Loader Jim',
            'pickup_spot': 'Spot A'
        }

        self.truck = create_truck(self.truck_data)
        self.driver = create_driver(self.driver_data)
        self.loader = create_loader(self.loader_data)

        self.crew_data = {
            'driver_id': self.driver.id,
            'loader_ids': [self.loader.id],
            'truck_id': self.truck.id
        }
        self.crew = create_crew(self.crew_data)

    def tearDown(self):
        # Clean up all created entities
        delete_crew(self.crew.id)
        delete_truck(self.truck.id)
        delete_driver(self.driver.id)
        delete_loader(self.loader.id)

    def test_create_crew_success(self):
        """Test if a crew can be successfully created"""
        crew = get_crew_by_id(self.crew.id)
        self.assertIsNotNone(crew, "Failed to create crew.")
        self.assertEqual(crew.driver_id, self.driver.id, "Crew driver mismatch.")
        self.assertIn(self.loader.id, crew.loader_ids, "Crew loader mismatch.")

    def test_create_crew_with_missing_truck(self):
        """Test if creating a crew with a missing truck should fail"""
        crew_data = self.crew_data.copy()
        crew_data['truck_id'] = None
        with self.assertRaises(ValueError, msg="Creating a crew without a truck should fail."):
            create_crew(crew_data)

    def test_delete_crew(self):
        """Test if a crew can be deleted successfully"""
        delete_crew(self.crew.id)
        crew = get_crew_by_id(self.crew.id)
        self.assertIsNone(crew, "Failed to delete crew.")

if __name__ == "__main__":
    unittest.main()