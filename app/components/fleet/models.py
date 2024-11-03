# components/fleet/models.py

from dataclasses import dataclass, field
from datetime import date
from typing import Optional, List  # Import List here
from fastlite import Database

# Initialize the FastLite database
db = Database('app_data.db')

@dataclass
class Truck:
    id: Optional[int] = field(default=None)
    truck_number: str = field(default="" )            # Unique Truck Identifier, e.g., T101, T201, etc.
    plate_number: str = field(default="")
    truck_type: str = field(default="")               # Types: Heavy-duty Garbage, Half-Ton, Flatbed
    capacity: int = field(default=0)                  # Capacity in kg
    status: str = field(default="Operational")        # Operational, Out of Service, Maintenance Due
    engine_hours: float = field(default=0.0)          # Engine hours
    mileage: int = field(default=0)                   # Mileage in km
    monthly_fuel_consumption: float = field(default=0.0)  # Monthly fuel consumption in liters
    fuel_efficiency: float = field(default=0.0)       # Fuel efficiency in km/l
    onboarding_date: Optional[date] = field(default=None)  # Date the truck was onboarded
    decommissioning_date: Optional[date] = field(default=None)  # Date the truck was decommissioned
    last_inspection_date: Optional[date] = field(default=None)  # Last yearly inspection date
    next_inspection_due: Optional[date] = field(default=None)   # Next inspection reminder
    emission_test_due: Optional[date] = field(default=None)     # Emission test reminder
    tire_change_due: Optional[date] = field(default=None)       # Tire change reminder
    brake_check_due: Optional[date] = field(default=None)       # Brake check reminder

    __tablename__ = 'trucks'

    @classmethod
    def create_table(cls):
        """Creates the trucks table if it doesn't exist."""
        query = f'''
        CREATE TABLE IF NOT EXISTS {cls.__tablename__} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            truck_number TEXT NOT NULL UNIQUE,
            plate_number TEXT NOT NULL UNIQUE,
            truck_type TEXT NOT NULL,
            capacity INTEGER NOT NULL,
            status TEXT NOT NULL,
            engine_hours REAL,
            mileage INTEGER,
            monthly_fuel_consumption REAL,
            fuel_efficiency REAL,
            onboarding_date DATE,
            decommissioning_date DATE,
            last_inspection_date DATE,
            next_inspection_due DATE,
            emission_test_due DATE,
            tire_change_due DATE,
            brake_check_due DATE
        )
        '''
        db.execute(query)

    @classmethod
    def find_all(cls) -> List['Truck']:
        """Fetches all trucks from the database."""
        query = f"SELECT * FROM {cls.__tablename__}"
        rows = db.q(query)
        return [cls(**cls._parse_row(row)) for row in rows]

    @classmethod
    def find_by_id(cls, truck_id: int) -> Optional['Truck']:
        """Finds a truck by ID."""
        query = f"SELECT * FROM {cls.__tablename__} WHERE id = ?"
        row = db.fetch_one(query, (truck_id,))
        return cls(**cls._parse_row(row)) if row else None

    @classmethod
    def find_by_truck_number(cls, truck_number: str) -> Optional['Truck']:
        """Finds a truck by its truck number."""
        query = f"SELECT * FROM {cls.__tablename__} WHERE truck_number = ?"
        row = db.fetch_one(query, (truck_number,))
        return cls(**cls._parse_row(row)) if row else None

    @classmethod
    def find_by_plate_number(cls, plate_number: str) -> Optional['Truck']:
        """Finds a truck by its plate number."""
        query = f"SELECT * FROM {cls.__tablename__} WHERE plate_number = ?"
        row = db.fetch_one(query, (plate_number,))
        return cls(**cls._parse_row(row)) if row else None

    def save(self) -> None:
        """Inserts or updates the truck in the database."""
        if self.id is None:
            # Insert new truck
            query = f'''
            INSERT INTO {self.__tablename__} (
                truck_number, plate_number, truck_type, capacity, status, engine_hours, mileage,
                monthly_fuel_consumption, fuel_efficiency, onboarding_date, decommissioning_date,
                last_inspection_date, next_inspection_due, emission_test_due, tire_change_due, brake_check_due
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
            params = (
                self.truck_number, self.plate_number, self.truck_type, self.capacity, self.status,
                self.engine_hours, self.mileage, self.monthly_fuel_consumption, self.fuel_efficiency,
                self.onboarding_date, self.decommissioning_date, self.last_inspection_date, self.next_inspection_due,
                self.emission_test_due, self.tire_change_due, self.brake_check_due
            )
            self.id = db.insert(query, params)
        else:
            # Update existing truck
            query = f'''
            UPDATE {self.__tablename__}
            SET truck_number = ?, plate_number = ?, truck_type = ?, capacity = ?, status = ?, engine_hours = ?,
                mileage = ?, monthly_fuel_consumption = ?, fuel_efficiency = ?, onboarding_date = ?, decommissioning_date = ?,
                last_inspection_date = ?, next_inspection_due = ?, emission_test_due = ?, tire_change_due = ?, brake_check_due = ?
            WHERE id = ?
            '''
            params = (
                self.truck_number, self.plate_number, self.truck_type, self.capacity, self.status,
                self.engine_hours, self.mileage, self.monthly_fuel_consumption, self.fuel_efficiency,
                self.onboarding_date, self.decommissioning_date, self.last_inspection_date, self.next_inspection_due,
                self.emission_test_due, self.tire_change_due, self.brake_check_due, self.id
            )
            db.execute(query, params)

    def delete(self) -> None:
        """Deletes the truck from the database."""
        query = f"DELETE FROM {self.__tablename__} WHERE id = ?"
        db.execute(query, (self.id,))

    @staticmethod
    def _parse_row(row) -> dict:
        """Parses a database row into a dictionary for initializing a Truck object."""
        return {
            'id': row['id'],
            'truck_number': row['truck_number'],
            'plate_number': row['plate_number'],
            'truck_type': row['truck_type'],
            'capacity': row['capacity'],
            'status': row['status'],
            'engine_hours': row['engine_hours'],
            'mileage': row['mileage'],
            'monthly_fuel_consumption': row['monthly_fuel_consumption'],
            'fuel_efficiency': row['fuel_efficiency'],
            'onboarding_date': row['onboarding_date'],
            'decommissioning_date': row['decommissioning_date'],
            'last_inspection_date': row['last_inspection_date'],
            'next_inspection_due': row['next_inspection_due'],
            'emission_test_due': row['emission_test_due'],
            'tire_change_due': row['tire_change_due'],
            'brake_check_due': row['brake_check_due'],
        }

    def __ft__(self):
        """Provides a FastHTML representation of the truck."""
        from fasthtml.common import Li, Div, A
        return Li(
            Div(f"Truck Number: {self.truck_number}"),
            Div(f"Plate Number: {self.plate_number}"),
            Div(f"Truck Type: {self.truck_type}"),
            Div(f"Capacity: {self.capacity} kg"),
            Div(f"Status: {self.status}"),
            Div(
                A("View", href=f"/fleet/view/{self.id}"),
                " | ",
                A("Edit", href=f"/fleet/edit/{self.id}"),
                " | ",
                A("Delete", href=f"/fleet/delete/{self.id}", hx_post=f"/fleet/delete/{self.id}",
                  hx_confirm="Are you sure?", hx_target="#fleet-list")
            )
        )