import unittest
from components.schedule.models import Schedule
from components.driver.models import Driver
from components.fleet.models import Truck
from datetime import date

class TestScheduleFleetDriverIntegration(unittest.TestCase):

    def setUp(self):
        # Driver setup
        self.driver = Driver(name='Test Driver', license_expiry_date='2025-01-01', last_medical_check='2023-01-01')
        self.driver.save()

        # Truck setup
        self.truck = Truck(truck_number='T202', plate_number='XYZ123', truck_type='Light-duty', capacity=1000, status='Operational')
        self.truck.save()

        # Schedule setup
        self.schedule_data = {
            'week_number': 42,
            'dow': 'Monday',
            'driver_id': self.driver.id,
            'truck_id': self.truck.id,
            'date_generated': date.today()
        }

    def test_schedule_driver_fleet_integration(self):
        # Create schedule with a driver and truck
        schedule = Schedule(**self.schedule_data)
        schedule.save()

        fetched_schedule = Schedule.find_by_id(schedule.id)
        self.assertEqual(fetched_schedule.driver_id, self.driver.id)
        self.assertEqual(fetched_schedule.truck_id, self.truck.id)

if __name__ == "__main__":
    unittest.main()