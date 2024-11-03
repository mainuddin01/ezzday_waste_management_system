import unittest
from components.event.models import Event

class TestEvent(unittest.TestCase):

    def setUp(self):
        self.event_data = {
            'name': 'Holiday',
            'description': 'Thanksgiving Day',
            'week_number': 42,
            'event_type': 'Holiday'
        }

    def test_create_event(self):
        event = Event(**self.event_data)
        event.save()
        fetched_event = Event.find_by_id(event.id)
        self.assertEqual(fetched_event.name, self.event_data['name'])

    def test_delete_event(self):
        event = Event(**self.event_data)
        event.save()
        event.delete()
        deleted_event = Event.find_by_id(event.id)
        self.assertIsNone(deleted_event)

if __name__ == "__main__":
    unittest.main()