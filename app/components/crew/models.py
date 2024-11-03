# components/crew/models.py

from dataclasses import dataclass, field
from typing import List, Optional
from fastlite import Database

# Initialize the FastLite database
db = Database('app_data.db')

@dataclass
class Crew:
    id: Optional[int] = field(default=None)
    driver_id: Optional[int] = field(default=None)  # Driver assigned to the crew
    truck_id: Optional[int] = field(default=None)   # Truck assigned to the crew
    loaders: List[int] = field(default_factory=list)  # Loaders assigned to the crew

    __tablename__ = 'crews'

    @classmethod
    def create_table(cls):
        """Creates the crews table if it doesn't exist."""
        query = f'''
        CREATE TABLE IF NOT EXISTS {cls.__tablename__} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            driver_id INTEGER NOT NULL,
            truck_id INTEGER NOT NULL,
            loaders TEXT,  -- Stored as a comma-separated list of loader IDs
            FOREIGN KEY (driver_id) REFERENCES drivers(id),
            FOREIGN KEY (truck_id) REFERENCES trucks(id)
        )
        '''
        db.execute(query)

    @classmethod
    def find_all(cls) -> List['Crew']:
        """Fetches all crews from the database."""
        query = f"SELECT * FROM {cls.__tablename__}"
        rows = db.q(query)
        return [cls(**cls._parse_row(row)) for row in rows]

    @classmethod
    def find_by_id(cls, crew_id: int) -> Optional['Crew']:
        """Finds a crew by ID."""
        query = f"SELECT * FROM {cls.__tablename__} WHERE id = ?"
        row = db.fetch_one(query, (crew_id,))
        return cls(**cls._parse_row(row)) if row else None

    def save(self) -> None:
        """Inserts or updates the crew in the database."""
        loaders_str = ','.join(map(str, self.loaders))
        if self.id is None:
            # Insert new crew
            query = f'''
            INSERT INTO {self.__tablename__} (driver_id, truck_id, loaders)
            VALUES (?, ?, ?)
            '''
            params = (self.driver_id, self.truck_id, loaders_str)
            self.id = db.insert(query, params)
        else:
            # Update existing crew
            query = f'''
            UPDATE {self.__tablename__}
            SET driver_id = ?, truck_id = ?, loaders = ?
            WHERE id = ?
            '''
            params = (self.driver_id, self.truck_id, loaders_str, self.id)
            db.execute(query, params)

    def delete(self) -> None:
        """Deletes the crew from the database."""
        query = f"DELETE FROM {self.__tablename__} WHERE id = ?"
        db.execute(query, (self.id,))

    @staticmethod
    def _parse_row(row) -> dict:
        """Parses a database row into a dictionary for initializing a Crew object."""
        loaders = row['loaders'].split(',') if row['loaders'] else []
        return {
            'id': row['id'],
            'driver_id': row['driver_id'],
            'truck_id': row['truck_id'],
            'loaders': list(map(int, loaders)) if loaders else []
        }

    def __ft__(self):
        """Provides a FastHTML representation of the crew."""
        from fasthtml.common import Li, Div, A
        return Li(
            Div(f"Crew ID: {self.id}"),
            Div(f"Driver ID: {self.driver_id}"),
            Div(f"Truck ID: {self.truck_id}"),
            Div(f"Loaders: {', '.join(map(str, self.loaders))}"),
            Div(
                A("Edit", href=f"/crews/edit/{self.id}"),
                " | ",
                A("Delete", href=f"/crews/delete/{self.id}", hx_post=f"/crews/delete/{self.id}",
                  hx_confirm="Are you sure?", hx_target="#crew-list")
            )
        )