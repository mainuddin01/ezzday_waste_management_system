import unittest
from components.route.models import Route
from components.driver.models import Driver
from components.loader.models import Loader
from components.assignment.models import Assignment
from components.crew.models import Crew
from components.fleet.models import Truck
from datetime import date

class TestRouteDriverLoaderAssignmentFleetIntegration(unittest.TestCase):

    def setUp(self):
        # Driver setup
        self.driver = Driver(name='Test Driver', license_expiry_date='2025-01-01', last_medical_check='2023-01-01')
        self.driver.save()

        # Loader setup
        self.loader_1 = Loader(name='Loader 1', pickup_spot='Zone A')
        self.loader_2 = Loader(name='Loader 2', pickup_spot='Zone B')
        self.loader_1.save()
        self.loader_2.save()

        # Truck setup
        self.truck = Truck(truck_number='T303', plate_number='ZZZ111', truck_type='Heavy-duty Flatbed', capacity=2500, status='Operational')
        self.truck.save()

        # Route setup
        self.route = Route(name='Route 202', zone_id=1, description='Heavy-duty route')
        self.route.save()

        # Crew setup
        self.crew = Crew(driver_id=self.driver.id, loader_ids=[self.loader_1.id, self.loader_2.id], fleet_id=self.truck.id, status='Ready')
        self.crew.save()

        # Assignment setup
        self.assignment = Assignment(crew_id=self.crew.id, route_id=self.route.id, client_id=1, zone_id=1, assignment_date=date.today())
        self.assignment.save()

    def test_integration(self):
        # Check all components linked correctly
        fetched_assignment = Assignment.find_by_id(self.assignment.id)
        self.assertEqual(fetched_assignment.crew_id, self.crew.id)
        self.assertEqual(fetched_assignment.route_id, self.route.id)

if __name__ == "__main__":
    unittest.main()