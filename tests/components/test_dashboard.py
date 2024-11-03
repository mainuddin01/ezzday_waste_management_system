import unittest
from components.dashboard.views import admin_dashboard_view

class TestDashboardViews(unittest.TestCase):
    def test_admin_dashboard_view(self):
        response = admin_dashboard_view()
        self.assertIn("Admin Dashboard", response.render())

if __name__ == '__main__':
    unittest.main()

