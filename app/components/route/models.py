# components/route/models.py

from dataclasses import dataclass, field
from typing import Optional, List
from fastlite import Database

# Initialize the FastLite database
db = Database('app_data.db')

@dataclass
class Route:
    id: int = field(default=None)
    name: str = field(default="")
    zone_id: int = field(default=None)  # Relationship with the zone
    description: str = field(default="")

    __tablename__ = 'routes'

    @classmethod
    def create_table(cls):
        """Creates the routes table if it doesn't exist."""
        query = f'''
        CREATE TABLE IF NOT EXISTS {cls.__tablename__} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            zone_id INTEGER NOT NULL,
            description TEXT,
            UNIQUE(name, zone_id)
        )
        '''
        db.execute(query)

    @classmethod
    def find_all(cls) -> List['Route']:
        """Fetches all routes from the database."""
        query = f"SELECT * FROM {cls.__tablename__}"
        rows = db.q(query)
        return [cls(**row) for row in rows]

    @classmethod
    def find_all_by_zone_id(cls, zone_id: int) -> List['Route']:
        """Fetches all routes related to a specific zone."""
        query = f"SELECT * FROM {cls.__tablename__} WHERE zone_id = ?"
        rows = db.fetch_all(query, (zone_id,))
        return [cls(**row) for row in rows]

    @classmethod
    def find_by_id(cls, route_id: int) -> Optional['Route']:
        """Finds a route by ID."""
        query = f"SELECT * FROM {cls.__tablename__} WHERE id = ?"
        row = db.fetch_one(query, (route_id,))
        if row:
            return cls(**row)
        return None

    @classmethod
    def find_by_name_and_zone(cls, name: str, zone_id: int) -> Optional['Route']:
        """Finds a route by name within a specific zone."""
        query = f"SELECT * FROM {cls.__tablename__} WHERE name = ? AND zone_id = ?"
        row = db.fetch_one(query, (name, zone_id))
        if row:
            return cls(**row)
        return None

    def save(self):
        """Inserts or updates the route in the database."""
        if self.id is None:
            query = f'''
            INSERT INTO {self.__tablename__} (name, zone_id, description)
            VALUES (?, ?, ?)
            '''
            params = (self.name, self.zone_id, self.description)
            self.id = db.insert(query, params)
        else:
            query = f'''
            UPDATE {self.__tablename__}
            SET name = ?, zone_id = ?, description = ?
            WHERE id = ?
            '''
            params = (self.name, self.zone_id, self.description, self.id)
            db.execute(query, params)

    def delete(self):
        """Deletes the route from the database."""
        query = f"DELETE FROM {self.__tablename__} WHERE id = ?"
        db.execute(query, (self.id,))

    def __ft__(self):
        """Provides a FastHTML representation of the route."""
        from fasthtml.common import Li, Div, A
        return Li(
            Div(f"Route Name: {self.name}"),
            Div(f"Description: {self.description}"),
            Div(
                A("Edit", href=f"/routes/edit/{self.id}"),
                " | ",
                A("Delete", href=f"/routes/delete/{self.id}", hx_post=f"/routes/delete/{self.id}",
                  hx_confirm="Are you sure?", hx_target="#route-list")
            )
        )