import unittest
from components.driver.models import Driver
from components.loader.models import Loader
from components.assignment.models import Assignment
from components.crew.models import Crew
from components.fleet.models import Truck

class TestDriverLoaderAssignmentIntegration(unittest.TestCase):

    def setUp(self):
        """Set up environment for driver, loader, and assignment integration."""
        # Set up driver, loader, truck, and crew
        self.driver = Driver(
            name="Integration Driver",
            license_expiry_date="2026-01-01",
            last_medical_check="2024-01-01"
        )
        self.driver.save()

        self.loader1 = Loader(name="Integration Loader 1", pickup_spot="Spot A")
        self.loader1.save()

        self.truck = Truck(
            truck_number="T201",
            plate_number="DEF456",
            truck_type="Light-duty Half-Ton Truck",
            capacity=500,
            status="Operational"
        )
        self.truck.save()

        self.crew = Crew(
            driver_id=self.driver.id,
            loader_ids=[self.loader1.id],
            fleet_id=self.truck.id
        )
        self.crew.save()

        self.assignment_data = {
            'crew_id': self.crew.id,
            'route_id': 1,
            'client_id': 1,
            'zone_id': 1,
            'assignment_date': '2024-11-01'
        }

    def tearDown(self):
        """Clean up after each test."""
        assignments = Assignment.find_all_for_date('2024-11-01')
        for assignment in assignments:
            assignment.delete()

        self.crew.delete()
        self.driver.delete()
        self.loader1.delete()
        self.truck.delete()

    def test_driver_loader_assignment(self):
        """Test assigning a driver and loader to an assignment."""
        assignment = Assignment(**self.assignment_data)
        assignment.save()

        # Validate assignment relationship
        self.assertEqual(assignment.crew_id, self.crew.id, "Crew should be assigned to the assignment correctly.")
        self.assertEqual(assignment.route_id, 1, "Route ID should match.")

if __name__ == "__main__":
    unittest.main()