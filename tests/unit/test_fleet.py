import unittest
from components.fleet.models import Truck

class TestFleet(unittest.TestCase):

    def setUp(self):
        self.truck_data = {
            'truck_number': 'T101',
            'plate_number': 'ABC1234',
            'truck_type': 'Heavy-duty Garbage Truck',
            'capacity': 1500,
            'status': 'Operational',
            'engine_hours': 500,
            'mileage': 20000,
            'monthly_fuel_consumption': 600,
            'fuel_efficiency': 5.5,
            'onboarding_date': '2023-01-01',
            'last_inspection_date': '2023-08-01'
        }

    def test_create_truck(self):
        truck = Truck(**self.truck_data)
        truck.save()
        fetched_truck = Truck.find_by_id(truck.id)
        self.assertEqual(fetched_truck.truck_number, self.truck_data['truck_number'])

    def test_update_truck_status(self):
        truck = Truck(**self.truck_data)
        truck.save()
        truck.status = 'Out of Service'
        truck.save()
        updated_truck = Truck.find_by_id(truck.id)
        self.assertEqual(updated_truck.status, 'Out of Service')

if __name__ == "__main__":
    unittest.main()