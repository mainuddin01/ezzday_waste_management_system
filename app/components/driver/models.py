# components/driver/models.py

from dataclasses import dataclass, field
from datetime import date
from typing import Optional, List  # Import List here
from fastlite import Database

# Initialize the FastLite database
db = Database('app_data.db')

@dataclass
class Driver:
    id: Optional[int] = field(default=None)
    name: str = field(default="")
    license_number: str = field(default="")
    license_expiry: Optional[date] = field(default=None)
    last_medical_check: Optional[date] = field(default=None)

    __tablename__ = 'drivers'

    @classmethod
    def create_table(cls):
        """Creates the drivers table if it doesn't exist."""
        query = f'''
        CREATE TABLE IF NOT EXISTS {cls.__tablename__} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            license_number TEXT NOT NULL UNIQUE,
            license_expiry DATE NOT NULL,
            last_medical_check DATE
        )
        '''
        db.execute(query)

    @classmethod
    def find_all(cls) -> List['Driver']:
        """Fetches all drivers from the database."""
        query = f"SELECT * FROM {cls.__tablename__}"
        rows = db.q(query)
        return [cls(**cls._parse_row(row)) for row in rows]

    @classmethod
    def find_by_id(cls, driver_id: int) -> Optional['Driver']:
        """Finds a driver by ID."""
        query = f"SELECT * FROM {cls.__tablename__} WHERE id = ?"
        row = db.fetch_one(query, (driver_id,))
        return cls(**cls._parse_row(row)) if row else None

    @classmethod
    def find_by_license_number(cls, license_number: str) -> Optional['Driver']:
        """Finds a driver by their license number."""
        query = f"SELECT * FROM {cls.__tablename__} WHERE license_number = ?"
        row = db.fetch_one(query, (license_number,))
        return cls(**cls._parse_row(row)) if row else None

    def save(self) -> None:
        """Inserts or updates the driver in the database."""
        if self.id is None:
            # Insert new driver
            query = f'''
            INSERT INTO {self.__tablename__} (name, license_number, license_expiry, last_medical_check)
            VALUES (?, ?, ?, ?)
            '''
            params = (self.name, self.license_number, self.license_expiry, self.last_medical_check)
            self.id = db.insert(query, params)
        else:
            # Update existing driver
            query = f'''
            UPDATE {self.__tablename__}
            SET name = ?, license_number = ?, license_expiry = ?, last_medical_check = ?
            WHERE id = ?
            '''
            params = (self.name, self.license_number, self.license_expiry, self.last_medical_check, self.id)
            db.execute(query, params)

    def delete(self) -> None:
        """Deletes the driver from the database."""
        query = f"DELETE FROM {self.__tablename__} WHERE id = ?"
        db.execute(query, (self.id,))

    @staticmethod
    def _parse_row(row) -> dict:
        """Parses a database row into a dictionary for initializing a Driver object."""
        return {
            'id': row['id'],
            'name': row['name'],
            'license_number': row['license_number'],
            'license_expiry': row['license_expiry'],
            'last_medical_check': row['last_medical_check']
        }

    def __ft__(self):
        """Provides a FastHTML representation of the driver."""
        from fasthtml.common import Li, Div, A
        return Li(
            Div(f"Driver ID: {self.id}"),
            Div(f"Name: {self.name}"),
            Div(f"License Number: {self.license_number}"),
            Div(f"License Expiry: {self.license_expiry}"),
            Div(f"Last Medical Check: {self.last_medical_check}"),
            Div(
                A("Edit", href=f"/drivers/edit/{self.id}"),
                " | ",
                A("Delete", href=f"/drivers/delete/{self.id}", hx_post=f"/drivers/delete/{self.id}",
                  hx_confirm="Are you sure?", hx_target="#driver-list")
            )
        )