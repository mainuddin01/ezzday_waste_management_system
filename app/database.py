# app/database.py

import sqlite3
import os
import logging

from config import settings  # Ensure you have a settings module with DATABASE_URL or similar

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, db_path: str):
        """
        Initializes the database connection.
        Args:
            db_path (str): Path to the SQLite database file.
        """
        try:
            self.connection = sqlite3.connect(
                db_path,
                check_same_thread=False,  # Allows usage across multiple threads
                isolation_level=None     # Autocommit mode
            )
            self.connection.row_factory = sqlite3.Row  # Access columns by name
            self.cursor = self.connection.cursor()
            self.execute("PRAGMA foreign_keys = ON")  # Enforce foreign key constraints
            logger.info(f"Connected to the database at {db_path}.")
        except Exception as e:
            logger.exception(f"Failed to connect to the database at {db_path}: {e}")
            raise

    def execute(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        """
        Executes a given SQL query with optional parameters.
        Args:
            query (str): The SQL query to execute.
            params (tuple): Parameters to substitute into the query.
        Returns:
            sqlite3.Cursor: The cursor after executing the query.
        """
        try:
            logger.debug(f"Executing query: {query} | Params: {params}")
            return self.cursor.execute(query, params)
        except sqlite3.OperationalError as e:
            logger.exception(f"OperationalError during query execution: {e}")
            raise
        except Exception as e:
            logger.exception(f"Error executing query: {e}")
            raise

    def commit(self) -> None:
        """
        Commits the current transaction.
        """
        try:
            self.connection.commit()
            logger.debug("Transaction committed successfully.")
        except Exception as e:
            logger.exception(f"Error during commit: {e}")
            raise

    def close(self) -> None:
        """
        Closes the database connection.
        """
        try:
            self.cursor.close()
            self.connection.close()
            logger.info("Database connection closed.")
        except Exception as e:
            logger.exception(f"Error closing the database connection: {e}")
            raise


# Initialize the FastLite database
def get_db_path() -> str:
    """
    Retrieves the database path from environment variables or settings.
    Returns:
        str: The path to the SQLite database file.
    """
    # Attempt to get DATABASE_URL from environment variables
    db_url = os.getenv("DATABASE_URL", settings.DATABASE_URL)  # Fallback to settings if env var not set

    if db_url.startswith("sqlite:///"):
        db_path = db_url.split("sqlite:///")[-1]
    elif db_url.startswith("sqlite://"):
        # Handle other sqlite URL formats if necessary
        db_path = db_url.split("sqlite://")[-1]
    else:
        # For other databases, you might need different handling
        db_path = db_url  # Placeholder; adjust as per your requirements

    return db_path


db_path = get_db_path()
db = Database(db_path)

logger.info("Database initialized.")

# Set busy timeout to avoid locking issues
try:
    db.execute("PRAGMA busy_timeout = 20000")  # 20 seconds
    logger.debug("Busy timeout set to 20000 milliseconds.")
except Exception as e:
    logger.exception(f"Failed to set busy timeout: {e}")
    raise