import unittest
from components.auth.service import register_user, authenticate_user, delete_user
from components.auth.models import User
from helper import validate_email

class TestAuth(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up any necessary resources for the entire test class."""
        print("Setting up TestAuth class resources...")

    def setUp(self):
        """Set up environment before each test method."""
        # User data for successful registration
        self.valid_data = {
            'username': 'testuser',
            'password': 'TestPassword123!',
            'role': 'Admin'
        }

        # Invalid user data for failed registration
        self.invalid_data = {
            'username': 'testuser',  # Existing username
            'password': '123',  # Weak password
            'role': 'Admin'
        }

        # Clean up any existing user with the same username before each test
        existing_user = User.find_by_username(self.valid_data['username'])
        if existing_user:
            delete_user(existing_user.id)

    def tearDown(self):
        """Clean up after each test method to ensure test isolation."""
        user = User.find_by_username(self.valid_data['username'])
        if user:
            delete_user(user.id)

    def test_register_user_success(self):
        """Test successful user registration."""
        try:
            register_user(self.valid_data)
            user = User.find_by_username('testuser')
            self.assertIsNotNone(user, "User should be successfully registered.")
            self.assertEqual(user.username, 'testuser', "Username should match the registered name.")
        except ValueError as e:
            self.fail(f"Unexpected error during registration: {str(e)}")

    def test_register_user_with_existing_username(self):
        """Test user registration with an already existing username."""
        register_user(self.valid_data)
        with self.assertRaises(ValueError, msg="Should raise ValueError when username already exists"):
            register_user(self.valid_data)

    def test_register_user_with_weak_password(self):
        """Test registration with a weak password (should fail)."""
        weak_password_data = self.valid_data.copy()
        weak_password_data['password'] = '123'  # Weak password
        with self.assertRaises(ValueError, msg="Should raise ValueError for weak password"):
            register_user(weak_password_data)

    def test_register_user_missing_fields(self):
        """Test registration with missing fields (should fail)."""
        missing_field_data = self.valid_data.copy()
        del missing_field_data['username']  # Missing username
        with self.assertRaises(ValueError, msg="Should raise ValueError when required fields are missing"):
            register_user(missing_field_data)

    def test_authenticate_user_success(self):
        """Test successful user authentication with valid credentials."""
        register_user(self.valid_data)
        user = authenticate_user('testuser', 'TestPassword123!')
        self.assertIsNotNone(user, "User should be authenticated successfully with valid credentials.")
        self.assertEqual(user.username, 'testuser', "Authenticated user should have the correct username.")

    def test_authenticate_user_failure(self):
        """Test unsuccessful user authentication with invalid credentials."""
        register_user(self.valid_data)
        user = authenticate_user('testuser', 'WrongPassword!')
        self.assertIsNone(user, "Authentication should fail with incorrect password.")

    def test_authenticate_unregistered_user(self):
        """Test authentication for a non-existent user."""
        user = authenticate_user('nonexistentuser', 'password')
        self.assertIsNone(user, "Authentication should fail for an unregistered user.")

    def test_validate_email_format(self):
        """Test email validation function for valid and invalid email formats."""
        valid_email = 'valid.email@example.com'
        invalid_email = 'invalid-email'

        self.assertTrue(validate_email(valid_email), f"Should return True for a valid email format: {valid_email}")
        self.assertFalse(validate_email(invalid_email), f"Should return False for an invalid email format: {invalid_email}")

        # Additional email test cases for edge cases
        self.assertTrue(validate_email('user+tag@example.com'), "Should handle emails with '+' symbol")
        self.assertTrue(validate_email('user.name@example.co.uk'), "Should handle emails with subdomains")
        self.assertFalse(validate_email('user@.com'), "Should return False for an email without domain")

    @classmethod
    def tearDownClass(cls):
        """Clean up resources after all test methods are executed."""
        print("Cleaning up TestAuth class resources...")

if __name__ == "__main__":
    unittest.main()