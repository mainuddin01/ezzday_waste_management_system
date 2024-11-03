import unittest
import requests

BASE_URL = "http://localhost:8000"

class TestE2EAuthFlow(unittest.TestCase):
    def test_user_registration_and_login(self):
        # Register User
        response = requests.post(f"{BASE_URL}/auth/register", json={
            "username": "testuser",
            "password": "password123",
            "role": "Admin"
        })
        self.assertEqual(response.status_code, 200)
        
        # Login User
        response = requests.post(f"{BASE_URL}/auth/login", json={
            "username": "testuser",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()