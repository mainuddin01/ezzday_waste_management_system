# components/loader/models.py
# models.py

from dataclasses import dataclass, field
from typing import Optional
from fastlite import Database

# Initialize the FastLite database
db = Database('app_data.db')

@dataclass
class Loader:
    id: int = field(default=None)
    name: str = field(default="")
    pickup_spot: str = field(default="")

    # Table name in the database
    __tablename__ = 'loaders'

    @classmethod
    def create_table(cls):
        """Creates the loaders table if it doesn't exist."""
        query = f'''
        CREATE TABLE IF NOT EXISTS {cls.__tablename__} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            pickup_spot TEXT NOT NULL
        )
        '''
        db.execute(query)

    @classmethod
    def find_all(cls):
        """Fetches all loaders from the database."""
        query = f"SELECT * FROM {cls.__tablename__}"
        rows = db.q(query)
        return [cls(**row) for row in rows]

    @classmethod
    def find_by_id(cls, loader_id: int) -> Optional['Loader']:
        """Finds a loader by ID."""
        query = f"SELECT * FROM {cls.__tablename__} WHERE id = ?"
        row = db.fetch_one(query, (loader_id,))
        if row:
            return cls(**row)
        return None

    @classmethod
    def find_by_name(cls, name: str) -> Optional['Loader']:
        """Finds a loader by name."""
        query = f"SELECT * FROM {cls.__tablename__} WHERE name = ?"
        row = db.q(query, (name,))
        if row:
            return cls(**row)
        return None

    def save(self):
        """Inserts or updates the loader in the database."""
        if self.id is None:
            # Insert new loader
            query = f'''
            INSERT INTO {self.__tablename__} (name, pickup_spot)
            VALUES (?, ?)
            '''
            params = (self.name, self.pickup_spot)
            self.id = db.insert(query, params)
        else:
            # Update existing loader
            query = f'''
            UPDATE {self.__tablename__}
            SET name = ?, pickup_spot = ?
            WHERE id = ?
            '''
            params = (self.name, self.pickup_spot, self.id)
            db.execute(query, params)

    def delete(self):
        """Deletes the loader from the database."""
        query = f"DELETE FROM {self.__tablename__} WHERE id = ?"
        db.execute(query, (self.id,))

    def __ft__(self):
        """Provides a FastHTML representation of the loader."""
        from fasthtml.common import Li, Div, A
        return Li(
            Div(f"Loader ID: {self.id}"),
            Div(f"Name: {self.name}"),
            Div(f"Pickup Spot: {self.pickup_spot}"),
            Div(
                A("Edit", href=f"/loaders/edit/{self.id}"),
                " | ",
                A("Delete", href=f"/loaders/delete/{self.id}", hx_post=f"/loaders/delete/{self.id}",
                  hx_confirm="Are you sure?", hx_target="#loader-list")
            )
        )