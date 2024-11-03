import unittest
from database import setup_database, get_db_connection

class TestDatabaseIntegration(unittest.TestCase):
    def setUp(self):
        setup_database()
        self.connection = get_db_connection()

    def test_database_connection(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        self.assertGreater(len(tables), 0)

    def tearDown(self):
        self.connection.close()

if __name__ == '__main__':
    unittest.main()