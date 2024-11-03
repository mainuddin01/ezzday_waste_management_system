import unittest
from components.crew.models import Crew
from components.driver.models import Driver
from components.loader.models import Loader
from components.fleet.models import Truck

class TestCrew(unittest.TestCase):

    def setUp(self):
        """Set up environment for testing crews."""
        self.driver = Driver(
            name="Test Driver",
            license_expiry_date="2025-10-10",
            last_medical_check="2023-01-10"
        )
        self.driver.save()

        self.loader1 = Loader(name="Loader 1", pickup_spot="Spot A")
        self.loader2 = Loader(name="Loader 2", pickup_spot="Spot B")
        self.loader1.save()
        self.loader2.save()

        self.truck = Truck(
            truck_number="T101",
            plate_number="ABC123",
            truck_type="Heavy-duty Garbage Truck",
            capacity=1000,
            status="Operational"
        )
        self.truck.save()

        self.crew_data = {
            'driver_id': self.driver.id,
            'loader_ids': [self.loader1.id, self.loader2.id],
            'fleet_id': self.truck.id
        }

    def tearDown(self):
        """Clean up after each test."""
        crews = Crew.find_all()
        for crew in crews:
            crew.delete()

        drivers = Driver.find_all()
        for driver in drivers:
            driver.delete()

        loaders = Loader.find_all()
        for loader in loaders:
            loader.delete()

        trucks = Truck.find_all()
        for truck in trucks:
            truck.delete()

    def test_create_crew_success(self):
        """Test creating a crew successfully."""
        crew = Crew(**self.crew_data)
        crew.save()
        saved_crew = Crew.find_by_id(crew.id)

        self.assertIsNotNone(saved_crew, "Crew should be successfully created.")
        self.assertEqual(saved_crew.driver_id, self.driver.id, "Driver ID should match.")

    def test_update_crew(self):
        """Test updating a crew."""
        crew = Crew(**self.crew_data)
        crew.save()

        new_loader = Loader(name="New Loader", pickup_spot="New Spot")
        new_loader.save()
        crew.loader_ids = [new_loader.id]
        crew.save()

        updated_crew = Crew.find_by_id(crew.id)
        self.assertEqual(len(updated_crew.loader_ids), 1, "Crew should have only one loader after update.")
        self.assertEqual(updated_crew.loader_ids[0], new_loader.id, "Loader ID should be updated.")

    def test_delete_crew(self):
        """Test deleting a crew."""
        crew = Crew(**self.crew_data)
        crew.save()

        crew.delete()
        deleted_crew = Crew.find_by_id(crew.id)

        self.assertIsNone(deleted_crew, "Crew should be deleted successfully.")

if __name__ == "__main__":
    unittest.main()