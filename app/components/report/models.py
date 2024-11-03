# components/report/models.py
# models.py

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from fastlite import Database
import json

# Initialize the FastLite database
db = Database('app_data.db')

@dataclass
class Report:
    id: int = field(default=None)
    report_type: str = field(default="")          # e.g., "End of Day", "Issue Report", etc.
    parameters: Optional[dict] = field(default_factory=dict)  # Parameters used to generate the report
    generated_at: datetime = field(default_factory=datetime.now)  # Date and time the report was generated
    file_path: str = field(default="")            # Path to the report file (PDF or CSV)

    # Table name in the database
    __tablename__ = 'reports'

    @classmethod
    def create_table(cls):
        """Creates the reports table if it doesn't exist."""
        query = f'''
        CREATE TABLE IF NOT EXISTS {cls.__tablename__} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_type TEXT NOT NULL,
            parameters TEXT,
            generated_at DATETIME NOT NULL,
            file_path TEXT NOT NULL
        )
        '''
        db.execute(query)

    @classmethod
    def find_all(cls):
        """Fetches all reports from the database."""
        query = f"SELECT * FROM {cls.__tablename__} ORDER BY generated_at DESC"
        rows = db.q(query)
        return [cls(**cls._parse_row(row)) for row in rows]

    @classmethod
    def find_by_id(cls, report_id: int) -> Optional['Report']:
        """Finds a report by ID."""
        query = f"SELECT * FROM {cls.__tablename__} WHERE id = ?"
        row = db.fetch_one(query, (report_id,))
        if row:
            return cls(**cls._parse_row(row))
        return None

    def save(self):
        """Inserts or updates the report in the database."""
        parameters_json = json.dumps(self.parameters) if self.parameters else ""
        if self.id is None:
            # Insert new report
            query = f'''
            INSERT INTO {self.__tablename__} (report_type, parameters, generated_at, file_path)
            VALUES (?, ?, ?, ?)
            '''
            params = (self.report_type, parameters_json, self.generated_at.strftime("%Y-%m-%d %H:%M:%S"), self.file_path)
            self.id = db.insert(query, params)
        else:
            # Update existing report
            query = f'''
            UPDATE {self.__tablename__}
            SET report_type = ?, parameters = ?, generated_at = ?, file_path = ?
            WHERE id = ?
            '''
            params = (self.report_type, parameters_json, self.generated_at.strftime("%Y-%m-%d %H:%M:%S"), self.file_path, self.id)
            db.execute(query, params)

    def delete(self):
        """Deletes the report from the database."""
        query = f"DELETE FROM {self.__tablename__} WHERE id = ?"
        db.execute(query, (self.id,))

    @staticmethod
    def _parse_row(row):
        """Parses a database row into a dictionary for initializing a Report object."""
        return {
            'id': row['id'],
            'report_type': row['report_type'],
            'parameters': json.loads(row['parameters']) if row['parameters'] else {},
            'generated_at': datetime.strptime(row['generated_at'], "%Y-%m-%d %H:%M:%S"),
            'file_path': row['file_path']
        }

    def __ft__(self):
        """Provides a FastHTML representation of the report."""
        from fasthtml.common import Li, Div, A
        return Li(
            Div(f"Report ID: {self.id}"),
            Div(f"Report Type: {self.report_type}"),
            Div(f"Generated At: {self.generated_at.strftime('%Y-%m-%d %H:%M:%S')}"),
            Div(f"File Path: {self.file_path}"),
            Div(
                A("View", href=f"/reports/view/{self.id}"),
                " | ",
                A("Delete", href=f"/reports/delete/{self.id}", hx_post=f"/reports/delete/{self.id}",
                  hx_confirm="Are you sure?", hx_target="#report-list")
            )
        )