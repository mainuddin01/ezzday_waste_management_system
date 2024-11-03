# components/event/models.py

from dataclasses import dataclass, field
from typing import List
from fastlite import Database
from datetime import date

# Initialize the FastLite database
db = Database('app_data.db')

@dataclass
class Event:
    id: int | None = field(default=None)
    name: str = field(default="")               # Name of the event (e.g., Holiday, Leaf Collection)
    description: str = field(default="")        # Description of the event
    start_date: date | None = field(default=None)      # Start date of the event
    end_date: date | None = field(default=None)        # End date of the event
    affected_clients: List[int] = field(default_factory=list)  # List of client IDs affected by the event
    event_type: str = field(default="")         # Type of event (e.g., Holiday, Leaf Collection)
    additional_info: str = field(default="")    # Additional information or notes about the event

    # Table name in the database
    __tablename__ = 'events'

    @classmethod
    def create_table(cls):
        """Creates the events table if it doesn't exist."""
        query = f'''
        CREATE TABLE IF NOT EXISTS {cls.__tablename__} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            affected_clients TEXT,  -- Stored as a comma-separated list of client IDs
            event_type TEXT NOT NULL,
            additional_info TEXT
        )
        '''
        db.execute(query)

    @classmethod
    def find_all(cls):
        """Fetches all events from the database."""
        query = f"SELECT * FROM {cls.__tablename__}"
        rows = db.q(query)
        return [cls(**cls._parse_row(row)) for row in rows]

    @classmethod
    def find_by_id(cls, event_id: int):
        """Finds an event by ID."""
        query = f"SELECT * FROM {cls.__tablename__} WHERE id = ?"
        row = db.q(query, (event_id,))
        return cls(**cls._parse_row(row)) if row else None

    def save(self):
        """Inserts or updates the event in the database."""
        affected_clients_str = ','.join(map(str, self.affected_clients))
        if self.id is None:
            # Insert new event
            query = f'''
            INSERT INTO {self.__tablename__} (name, description, start_date, end_date, affected_clients, event_type, additional_info)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            '''
            params = (self.name, self.description, self.start_date, self.end_date, affected_clients_str, self.event_type, self.additional_info)
            self.id = db.insert(query, params)
        else:
            # Update existing event
            query = f'''
            UPDATE {self.__tablename__}
            SET name = ?, description = ?, start_date = ?, end_date = ?, affected_clients = ?, event_type = ?, additional_info = ?
            WHERE id = ?
            '''
            params = (self.name, self.description, self.start_date, self.end_date, affected_clients_str, self.event_type, self.additional_info, self.id)
            db.execute(query, params)

    def delete(self):
        """Deletes the event from the database."""
        query = f"DELETE FROM {self.__tablename__} WHERE id = ?"
        db.execute(query, (self.id,))

    @staticmethod
    def _parse_row(row):
        """Parses a database row into a dictionary for initializing an Event object."""
        affected_clients = row['affected_clients'].split(',') if row['affected_clients'] else []
        return {
            'id': row['id'],
            'name': row['name'],
            'description': row['description'],
            'start_date': row['start_date'],
            'end_date': row['end_date'],
            'affected_clients': list(map(int, affected_clients)) if affected_clients else [],
            'event_type': row['event_type'],
            'additional_info': row['additional_info']
        }

    def __ft__(self):
        """Provides a FastHTML representation of the event."""
        from fasthtml.common import Li, Div, A
        return Li(
            Div(f"Event: {self.name}"),
            Div(f"Description: {self.description}"),
            Div(f"Start Date: {self.start_date}"),
            Div(f"End Date: {self.end_date}"),
            Div(f"Event Type: {self.event_type}"),
            Div(
                A("Edit", href=f"/events/edit/{self.id}"),
                " | ",
                A("Delete", href=f"/events/delete/{self.id}", hx_post=f"/events/delete/{self.id}",
                  hx_confirm="Are you sure?", hx_target="#event-list")
            )
        )