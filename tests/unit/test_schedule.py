import unittest
from components.schedule.models import Schedule
from datetime import date

class TestSchedule(unittest.TestCase):

    def setUp(self):
        self.schedule_data = {
            'week_number': 42,
            'dow': 'Tuesday',
            'driver_id': 1,
            'loader_ids': [2, 3],
            'assignment_id': 1,
            'notification_sent': False,
            'attendance_marked': False,
            'date_generated': date.today()
        }

    def test_create_schedule(self):
        schedule = Schedule(**self.schedule_data)
        schedule.save()
        fetched_schedule = Schedule.find_by_id(schedule.id)
        self.assertEqual(fetched_schedule.week_number, self.schedule_data['week_number'])

    def test_delete_schedule(self):
        schedule = Schedule(**self.schedule_data)
        schedule.save()
        schedule.delete()
        deleted_schedule = Schedule.find_by_id(schedule.id)
        self.assertIsNone(deleted_schedule)

if __name__ == "__main__":
    unittest.main()