# app/components/auth/models.py

from dataclasses import dataclass, field
from typing import Optional, List
import bcrypt
import logging

# Import the shared database instance
from app.database import db

logger = logging.getLogger(__name__)


@dataclass
class User:
    id: Optional[int] = field(default=None)
    username: str = field(default="")
    password_hash: str = field(default="")  # Store hashed passwords
    role: str = field(default="")            # Role of the user, e.g., Admin, Supervisor, Dispatch

    __tablename__ = 'users'

    @classmethod
    def create_table(cls):
        """Creates the users table if it doesn't exist."""
        query = f'''
        CREATE TABLE IF NOT EXISTS {cls.__tablename__} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL
        )
        '''
        try:
            db.execute(query)
            db.commit()
            logger.info(f"Table '{cls.__tablename__}' ensured in database.")
        except Exception as e:
            logger.exception(f"Error creating table '{cls.__tablename__}': {e}")
            raise

    @classmethod
    def find_all(cls) -> List['User']:
        """Fetches all users from the database."""
        query = f"SELECT * FROM {cls.__tablename__}"
        try:
            rows = db.execute(query).fetchall()
            return [cls(**row) for row in rows]
        except Exception as e:
            logger.exception(f"Error fetching users")
            return None

    @classmethod
    def find_by_username(cls, username: str) -> Optional['User']:
        """Finds a user by their username."""
        query = f"SELECT * FROM {cls.__tablename__} WHERE username = ?"
        try:
            row = db.execute(query, (username,)).fetchone()
            if row:
                logger.debug(f"User found: {username}")
                return cls(**row)
            logger.debug(f"User not found: {username}")
            return None
        except Exception as e:
            logger.exception(f"Error fetching user by username '{username}': {e}")
            return None

    @classmethod
    def find_by_id(cls, user_id: int) -> Optional['User']:
        """Finds a user by their ID."""
        query = f"SELECT * FROM {cls.__tablename__} WHERE id = ?"
        try:
            row = db.execute(query, (user_id,)).fetchone()
            if row:
                logger.debug(f"User found by ID: {user_id}")
                return cls(**row)
            logger.debug(f"User not found by ID: {user_id}")
            return None
        except Exception as e:
            logger.exception(f"Error fetching user by ID '{user_id}': {e}")
            return None

    def save(self) -> None:
        """Inserts or updates the user in the database."""
        if self.id is None:
            # Insert new user
            query = f'''
            INSERT INTO {self.__tablename__} (username, password_hash, role)
            VALUES (?, ?, ?)
            '''
            params = (self.username, self.password_hash, self.role)
            try:
                db.execute(query, params)
                self.id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
                db.commit()
                logger.info(f"New user created: {self.username} with ID: {self.id}")
            except Exception as e:
                logger.exception(f"Error inserting user '{self.username}': {e}")
                raise
        else:
            # Update existing user
            query = f'''
            UPDATE {self.__tablename__}
            SET username = ?, password_hash = ?, role = ?
            WHERE id = ?
            '''
            params = (self.username, self.password_hash, self.role, self.id)
            try:
                db.execute(query, params)
                db.commit()
                logger.info(f"User updated: {self.username} with ID: {self.id}")
            except Exception as e:
                logger.exception(f"Error updating user '{self.username}': {e}")
                raise

    def set_password(self, password: str) -> None:
        """Hashes and sets the user's password."""
        try:
            self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            logger.debug(f"Password set for user: {self.username}")
        except Exception as e:
            logger.exception(f"Error hashing password for user '{self.username}': {e}")
            raise

    def verify_password(self, password: str) -> bool:
        """Verifies a password against the stored password hash."""
        try:
            is_correct = bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
            logger.debug(f"Password verification for user '{self.username}': {is_correct}")
            return is_correct
        except Exception as e:
            logger.exception(f"Error verifying password for user '{self.username}': {e}")
            return False