# components/assignment/models.py

from dataclasses import dataclass, field
from datetime import datetime, date, time
from fastlite import Database

# Initialize the FastLite database
db = Database('app_data.db')

@dataclass
class Assignment:
    id: int | None = field(default=None)
    crew_id: int | None = field(default=None)       # Relationship with Crew
    route_id: int | None = field(default=None)      # Relationship with Route
    client_id: int | None = field(default=None)     # Relationship with Client
    zone_id: int | None = field(default=None)       # Relationship with Zone
    week_number: int = field(default_factory=lambda: date.today().isocalendar()[1])  # Current week number
    doc: date = field(default_factory=date.today)  # Date of collection
    dow: str = field(default_factory=lambda: date.today().strftime("%A"))  # Day of the week
    week_type: str = field(default="Regular")  # Regular or Event
    start_time: time = field(default_factory=lambda: time(6, 30))  # Default start time at 6:30 AM
    end_time: time | None = field(default=None)       # End time to be recorded at the end of the day
    completion_time: float = field(default=0.0)  # Completion time in hours
    attendance_confirmed: bool = field(default=False)  # Attendance confirmation
    ppe_compliance: bool = field(default=False)        # PPE compliance confirmation
    status_updates: dict = field(default_factory=lambda: {"11AM": None, "1PM": None, "3PM": None, "EOD": None})

    # Table name in the database
    __tablename__ = 'assignments'

    @classmethod
    def create_table(cls):
        """Creates the assignments table if it doesn't exist."""
        query = f'''
        CREATE TABLE IF NOT EXISTS {cls.__tablename__} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            crew_id INTEGER NOT NULL,
            route_id INTEGER NOT NULL,
            client_id INTEGER NOT NULL,
            zone_id INTEGER NOT NULL,
            week_number INTEGER NOT NULL,
            doc DATE NOT NULL,
            dow TEXT NOT NULL,
            week_type TEXT NOT NULL,
            start_time TIME NOT NULL,
            end_time TIME,
            completion_time REAL,
            attendance_confirmed BOOLEAN NOT NULL,
            ppe_compliance BOOLEAN NOT NULL,
            status_updates TEXT
        )
        '''
        db.execute(query)

    @classmethod
    def find_all_for_date(cls, assignment_date: date):
        """Fetches all assignments for a specific date."""
        query = f"SELECT * FROM {cls.__tablename__} WHERE doc = ?"
        rows = db.q(query, (assignment_date.format(),))  # Ensure date is in string format
        return [cls(**row) for row in rows]

    @classmethod
    def find_by_id(cls, assignment_id: int):
        """Fetches an assignment by its ID."""
        query = f"SELECT * FROM {cls.__tablename__} WHERE id = ?"
        row = db.q(query, (assignment_id,))
        return cls(**row) if row else None

    def save(self):
        """Inserts or updates the assignment in the database."""
        if self.id is None:
            # Insert new assignment
            query = f'''
            INSERT INTO {self.__tablename__} (crew_id, route_id, client_id, zone_id, week_number, doc, dow, week_type,
                                              start_time, end_time, completion_time, attendance_confirmed, ppe_compliance, status_updates)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
            params = (
                self.crew_id, self.route_id, self.client_id, self.zone_id, self.week_number, self.doc.isoformat(),
                self.dow, self.week_type, self.start_time.strftime("%H:%M:%S"),
                self.end_time.strftime("%H:%M:%S") if self.end_time else None,
                self.completion_time, int(self.attendance_confirmed), int(self.ppe_compliance), str(self.status_updates)
            )
            self.id = db.insert(query, params)
        else:
            # Update existing assignment
            query = f'''
            UPDATE {self.__tablename__}
            SET crew_id = ?, route_id = ?, client_id = ?, zone_id = ?, week_number = ?, doc = ?, dow = ?, week_type = ?,
                start_time = ?, end_time = ?, completion_time = ?, attendance_confirmed = ?, ppe_compliance = ?, status_updates = ?
            WHERE id = ?
            '''
            params = (
                self.crew_id, self.route_id, self.client_id, self.zone_id, self.week_number, self.doc.isoformat(),
                self.dow, self.week_type, self.start_time.strftime("%H:%M:%S"),
                self.end_time.strftime("%H:%M:%S") if self.end_time else None,
                self.completion_time, int(self.attendance_confirmed), int(self.ppe_compliance),
                str(self.status_updates), self.id
            )
            db.execute(query, params)

    def delete(self):
        """Deletes the assignment from the database."""
        query = f"DELETE FROM {self.__tablename__} WHERE id = ?"
        db.execute(query, (self.id,))

    def mark_attendance(self, attendance: bool, ppe_compliance: bool):
        """Marks attendance and PPE compliance."""
        self.attendance_confirmed = attendance
        self.ppe_compliance = ppe_compliance
        self.save()

    def update_status(self, time_label: str, status: str):
        """Updates the status at a specific time label."""
        if time_label in self.status_updates:
            self.status_updates[time_label] = status
            self.save()

    def mark_completion(self, end_time: time):
        """Marks the assignment as completed and calculates completion time."""
        self.end_time = end_time
        start_datetime = datetime.combine(self.doc, self.start_time)
        end_datetime = datetime.combine(self.doc, end_time)
        self.completion_time = (end_datetime - start_datetime).total_seconds() / 3600  # In hours
        self.save()

    def __ft__(self):
        """Provides a FastHTML representation of the assignment."""
        from fasthtml.common import Li, Div, A
        return Li(
            Div(f"Assignment ID: {self.id}"),
            Div(f"Crew ID: {self.crew_id}"),
            Div(f"Route ID: {self.route_id}"),
            Div(f"Client ID: {self.client_id}"),
            Div(f"Zone ID: {self.zone_id}"),
            Div(f"Week Number: {self.week_number}"),
            Div(f"Date of Collection: {self.doc}"),
            Div(f"Day of Week: {self.dow}"),
            Div(f"Week Type: {self.week_type}"),
            Div(f"Start Time: {self.start_time.strftime('%H:%M:%S')}"),
            Div(f"End Time: {self.end_time.strftime('%H:%M:%S') if self.end_time else 'Not Completed'}"),
            Div(f"Completion Time: {self.completion_time:.2f} hours"),
            Div(f"Attendance Confirmed: {'Yes' if self.attendance_confirmed else 'No'}"),
            Div(f"PPE Compliance: {'Yes' if self.ppe_compliance else 'No'}"),
            Div(f"Status Updates: {self.status_updates}"),
            Div(
                A("Edit", href=f"/assignments/edit/{self.id}"),
                " | ",
                A("Delete", href=f"/assignments/delete/{self.id}", hx_post=f"/assignments/delete/{self.id}",
                  hx_confirm="Are you sure?", hx_target="#assignment-list")
            )
        )