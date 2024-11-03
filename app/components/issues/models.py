# components/issues/models.py

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from fastlite import Database

# Initialize the FastLite database
db = Database('app_data.db')

@dataclass
class Issue:
    id: int | None = field(default=None)
    crew_id: int = field(default=None)            # Crew that encountered the issue
    route_id: int = field(default=None)           # Route ID on which the issue was encountered
    address: str = field(default="")              # Address where the issue occurred
    description: str = field(default="")          # Issue description
    issue_type: str = field(default="")           # Type of issue (e.g., "Nothing Out", "Wrong Collection Week")
    date_reported: datetime = field(default_factory=datetime.now)  # Date and time of issue occurrence
    repeat_offender: bool = field(default=False)  # Flag indicating if the issue is part of a repeat pattern

    # Table name in the database
    __tablename__ = 'issues'

    @classmethod
    def create_table(cls):
        """Creates the issues table if it doesn't exist."""
        query = f'''
        CREATE TABLE IF NOT EXISTS {cls.__tablename__} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            crew_id INTEGER NOT NULL,
            route_id INTEGER NOT NULL,
            address TEXT NOT NULL,
            description TEXT,
            issue_type TEXT NOT NULL,
            date_reported DATETIME NOT NULL,
            repeat_offender BOOLEAN DEFAULT 0
        )
        '''
        db.execute(query)

    @classmethod
    def find_all(cls) -> List['Issue']:
        """Fetches all issues from the database."""
        query = f"SELECT * FROM {cls.__tablename__}"
        rows = db.fetch_all(query)
        return [cls(**cls._parse_row(row)) for row in rows]

    @classmethod
    def find_repeat_offenders(cls) -> List[str]:
        """Identify repeat offenders by tracking issues with the same address multiple times."""
        query = f'''
        SELECT address, COUNT(*) AS occurrences
        FROM {cls.__tablename__}
        GROUP BY address
        HAVING occurrences > 1
        '''
        rows = db.fetch_all(query)
        repeat_addresses = [row['address'] for row in rows]

        # Update issues that have a repeat offender flag
        if repeat_addresses:
            update_query = f'''
            UPDATE {cls.__tablename__}
            SET repeat_offender = 1
            WHERE address IN ({','.join(['?' for _ in repeat_addresses])})
            '''
            db.execute(update_query, repeat_addresses)

        return repeat_addresses

    @classmethod
    def find_by_id(cls, issue_id: int) -> Optional['Issue']:
        """Finds an issue by ID."""
        query = f"SELECT * FROM {cls.__tablename__} WHERE id = ?"
        row = db.fetch_one(query, (issue_id,))
        return cls(**cls._parse_row(row)) if row else None

    def save(self) -> None:
        """Inserts or updates the issue in the database, checking for repeat offenders."""
        if self.id is None:
            # Insert new issue
            query = f'''
            INSERT INTO {self.__tablename__} (
                crew_id, route_id, address, description, issue_type, date_reported, repeat_offender
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            '''
            params = (
                self.crew_id, self.route_id, self.address, self.description, self.issue_type,
                self.date_reported.strftime("%Y-%m-%d %H:%M:%S"), int(self.repeat_offender)
            )
            self.id = db.insert(query, params)
        else:
            # Update existing issue
            query = f'''
            UPDATE {self.__tablename__}
            SET crew_id = ?, route_id = ?, address = ?, description = ?, issue_type = ?, date_reported = ?, repeat_offender = ?
            WHERE id = ?
            '''
            params = (
                self.crew_id, self.route_id, self.address, self.description, self.issue_type,
                self.date_reported.strftime("%Y-%m-%d %H:%M:%S"), int(self.repeat_offender), self.id
            )
            db.execute(query, params)

        # Check if the address should be marked as a repeat offender
        self._check_repeat_offender()

    def delete(self) -> None:
        """Deletes the issue from the database."""
        query = f"DELETE FROM {self.__tablename__} WHERE id = ?"
        db.execute(query, (self.id,))

    def _check_repeat_offender(self) -> None:
        """Check if this issue should be marked as a repeat offender."""
        query = f'''
        SELECT COUNT(*) AS occurrences
        FROM {self.__tablename__}
        WHERE address = ?
        '''
        row = db.fetch_one(query, (self.address,))
        count = row['occurrences']
        self.repeat_offender = count > 1

        # Update the issue with the repeat offender status if necessary
        update_query = f'''
        UPDATE {self.__tablename__}
        SET repeat_offender = ?
        WHERE address = ?
        '''
        db.execute(update_query, (int(self.repeat_offender), self.address))

    @staticmethod
    def _parse_row(row):
        """Parses a database row into a dictionary for initializing an Issue object."""
        return {
            'id': row['id'],
            'crew_id': row['crew_id'],
            'route_id': row['route_id'],
            'address': row['address'],
            'description': row['description'],
            'issue_type': row['issue_type'],
            'date_reported': datetime.strptime(row['date_reported'], "%Y-%m-%d %H:%M:%S"),
            'repeat_offender': bool(row['repeat_offender'])
        }

    def __ft__(self):
        """Provides a FastHTML representation of the issue."""
        from fasthtml.common import Li, Div, A
        return Li(
            Div(f"Issue ID: {self.id}"),
            Div(f"Crew ID: {self.crew_id}"),
            Div(f"Route ID: {self.route_id}"),
            Div(f"Address: {self.address}"),
            Div(f"Description: {self.description}"),
            Div(f"Issue Type: {self.issue_type}"),
            Div(f"Date Reported: {self.date_reported.strftime('%Y-%m-%d %H:%M:%S')}"),
            Div(f"Repeat Offender: {'Yes' if self.repeat_offender else 'No'}"),
            Div(
                A("Edit", href=f"/issues/edit/{self.id}"),
                " | ",
                A("Delete", href=f"/issues/delete/{self.id}", hx_post=f"/issues/delete/{self.id}",
                  hx_confirm="Are you sure?", hx_target="#issue-list")
            )
        )