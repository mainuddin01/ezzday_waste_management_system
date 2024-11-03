# components/zone/models.py

from dataclasses import dataclass, field
from typing import List, Optional
from fastlite import Database
from datetime import datetime

# Initialize the FastLite database
db = Database('app_data.db')

@dataclass
class Zone:
    id: int = field(default=None)
    name: str = field(default="")
    client_id: int = field(default=None)  # Relationship with the client
    description: str = field(default="")
    created_at: datetime = field(default_factory=datetime.now)
    routes: List['Route'] = field(default_factory=list)  # Relationship with routes

    __tablename__ = 'zones'

    @classmethod
    def create_table(cls):
        """Creates the zones table if it doesn't exist."""
        query = f'''
        CREATE TABLE IF NOT EXISTS {cls.__tablename__} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            client_id INTEGER NOT NULL,
            description TEXT,
            created_at DATETIME NOT NULL,
            UNIQUE(name, client_id)
        )
        '''
        db.execute(query)

    @classmethod
    def find_all(cls) -> List['Zone']:
        """Fetches all zones from the database."""
        query = f"SELECT * FROM {cls.__tablename__} ORDER BY created_at DESC"
        rows = db.fetch_all(query)
        return [cls(**row) for row in rows]

    @classmethod
    def find_by_id(cls, zone_id: int) -> Optional['Zone']:
        """Finds a zone by ID."""
        query = f"SELECT * FROM {cls.__tablename__} WHERE id = ?"
        row = db.fetch_one(query, (zone_id,))
        if row:
            zone = cls(**row)
            # Fetch routes when needed
            from app.components.route.models import Route  # Import inside method
            zone.routes = Route.find_all_by_zone_id(zone_id)
            return zone
        return None

    @classmethod
    def find_by_name_and_client(cls, name: str, client_id: int) -> Optional['Zone']:
        """Finds a zone by name within a specific client."""
        query = f"SELECT * FROM {cls.__tablename__} WHERE name = ? AND client_id = ?"
        row = db.fetch_one(query, (name, client_id))
        if row:
            return cls(**row)
        return None

    def save(self):
        """Inserts or updates the zone in the database."""
        if self.id is None:
            query = f'''
            INSERT INTO {self.__tablename__} (name, client_id, description, created_at)
            VALUES (?, ?, ?, ?)
            '''
            params = (self.name, self.client_id, self.description, self.created_at.strftime("%Y-%m-%d %H:%M:%S"))
            self.id = db.insert(query, params)
        else:
            query = f'''
            UPDATE {self.__tablename__}
            SET name = ?, client_id = ?, description = ?
            WHERE id = ?
            '''
            params = (self.name, self.client_id, self.description, self.id)
            db.execute(query, params)

    def delete(self):
        """Deletes the zone from the database."""
        query = f"DELETE FROM {self.__tablename__} WHERE id = ?"
        db.execute(query, (self.id,))

    def __ft__(self):
        """Provides a FastHTML representation of the zone."""
        from fasthtml.common import Li, Div, A
        return Li(
            Div(f"Zone Name: {self.name}"),
            Div(f"Description: {self.description}"),
            Div(
                A("View Routes", href=f"/zones/{self.id}/routes"),
                " | ",
                A("Edit", href=f"/zones/edit/{self.id}"),
                " | ",
                A("Delete", href=f"/zones/delete/{self.id}", hx_post=f"/zones/delete/{self.id}",
                  hx_confirm="Are you sure?", hx_target="#zone-list")
            )
        )