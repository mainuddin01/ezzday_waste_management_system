# components/client/models.py

from dataclasses import dataclass, field
from typing import List, Optional
from fastlite import Database

# Initialize the FastLite database
db = Database('app_data.db')

@dataclass
class Client:
    id: Optional[int] = field(default=None)
    name: str = field(default="")
    client_type: str = field(default="")  # e.g., Contractors, Subcontractors, etc.
    description: str = field(default="")  # Additional information about the client
    contact_name: str = field(default="")  # Name of the contact person
    contact_phone: str = field(default="")  # Contact phone number
    contact_email: str = field(default="")  # Contact email
    zones_serviced: List[int] = field(default_factory=list)  # List of zone IDs

    __tablename__ = 'clients'

    @classmethod
    def create_table(cls):
        """Creates the clients table if it doesn't exist."""
        query = f'''
        CREATE TABLE IF NOT EXISTS {cls.__tablename__} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            client_type TEXT NOT NULL,
            description TEXT,
            contact_name TEXT,
            contact_phone TEXT,
            contact_email TEXT,
            zones_serviced TEXT  -- Stored as a comma-separated list of zone IDs
        )
        '''
        db.execute(query)

    @classmethod
    def find_all(cls) -> List['Client']:
        """Fetches all clients from the database."""
        query = f"SELECT * FROM {cls.__tablename__}"
        rows = db.q(query)
        return [cls(**cls._parse_row(row)) for row in rows]

    @classmethod
    def find_by_id(cls, client_id: int) -> Optional['Client']:
        """Finds a client by ID."""
        query = f"SELECT * FROM {cls.__tablename__} WHERE id = ?"
        row = db.fetch_one(query, (client_id,))
        return cls(**cls._parse_row(row)) if row else None

    def save(self) -> None:
        """Inserts or updates the client in the database."""
        zones_serviced_str = ','.join(map(str, self.zones_serviced))
        if self.id is None:
            # Insert new client
            query = f'''
            INSERT INTO {self.__tablename__} (name, client_type, description, contact_name, contact_phone, contact_email, zones_serviced)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            '''
            params = (
                self.name,
                self.client_type,
                self.description,
                self.contact_name,
                self.contact_phone,
                self.contact_email,
                zones_serviced_str
            )
            self.id = db.insert(query, params)
        else:
            # Update existing client
            query = f'''
            UPDATE {self.__tablename__}
            SET name = ?, client_type = ?, description = ?, contact_name = ?, contact_phone = ?, contact_email = ?, zones_serviced = ?
            WHERE id = ?
            '''
            params = (
                self.name,
                self.client_type,
                self.description,
                self.contact_name,
                self.contact_phone,
                self.contact_email,
                zones_serviced_str,
                self.id
            )
            db.execute(query, params)

    def delete(self) -> None:
        """Deletes the client from the database."""
        query = f"DELETE FROM {self.__tablename__} WHERE id = ?"
        db.execute(query, (self.id,))

    @staticmethod
    def _parse_row(row) -> dict:
        """Parses a database row into a dictionary for initializing a Client object."""
        zones_serviced = row['zones_serviced'].split(',') if row['zones_serviced'] else []
        return {
            'id': row['id'],
            'name': row['name'],
            'client_type': row['client_type'],
            'description': row['description'],
            'contact_name': row['contact_name'],
            'contact_phone': row['contact_phone'],
            'contact_email': row['contact_email'],
            'zones_serviced': list(map(int, zones_serviced)) if zones_serviced else []
        }

    def __ft__(self):
        """Provides a FastHTML representation of the client."""
        from fasthtml.common import Li, Div, A
        return Li(
            Div(f"Client Name: {self.name}"),
            Div(f"Type: {self.client_type}"),
            Div(f"Contact: {self.contact_name}, {self.contact_phone}, {self.contact_email}"),
            Div(f"Zones Serviced: {', '.join(map(str, self.zones_serviced))}"),
            Div(
                A("Edit", href=f"/clients/edit/{self.id}"),
                " | ",
                A("Delete", href=f"/clients/delete/{self.id}", hx_post=f"/clients/delete/{self.id}",
                  hx_confirm="Are you sure?", hx_target="#client-list")
            )
        )