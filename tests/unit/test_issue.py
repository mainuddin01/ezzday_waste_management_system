import unittest
from components.issue.models import Issue

class TestIssue(unittest.TestCase):

    def setUp(self):
        self.issue_data = {
            'crew_id': 1,
            'route_id': 1,
            'address': '123 Test Street',
            'description': 'Nothing Out',
            'issue_type': 'Missed Collection',
            'repeat_offender': False
        }

    def test_report_issue(self):
        issue = Issue(**self.issue_data)
        issue.save()
        fetched_issue = Issue.find_by_id(issue.id)
        self.assertEqual(fetched_issue.address, self.issue_data['address'])

    def test_mark_repeat_offender(self):
        issue = Issue(**self.issue_data)
        issue.save()
        issue.repeat_offender = True
        issue.save()
        updated_issue = Issue.find_by_id(issue.id)
        self.assertTrue(updated_issue.repeat_offender)

if __name__ == "__main__":
    unittest.main()