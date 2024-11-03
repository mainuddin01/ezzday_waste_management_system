import unittest
from components.fleet.models import Truck

class TestFleetModel(unittest.TestCase):
    def setUp(self):
        self.truck = Truck(
            id=1,
            truck_number="T101",
            plate_number="ABC123",
            truck_type="Heavy-duty Garbage Truck",
            capacity=10000
        )

    def test_truck_creation(self):
        self.assertEqual(self.truck.truck_number, "T101")
        self.assertEqual(self.truck.truck_type, "Heavy-duty Garbage Truck")

if __name__ == '__main__':
    unittest.main()
