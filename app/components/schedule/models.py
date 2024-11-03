# components/schedule/models.py

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from fastlite import Database

# Initialize the FastLite database
db = Database('app_data.db')

@dataclass
class Schedule:
    id: int = field(default=None)
    week_number: int = field(default=None)              # Week number of the schedule
    dow: str = field(default="")                        # Day of the week (e.g., "Monday")
    driver_id: int = field(default=None)                # Assigned Driver ID
    loader_ids: List[int] = field(default_factory=list) # Assigned Loader IDs
    notification_sent: bool = field(default=False)      # Whether notifications have been sent
    schedule_created_at: datetime = field(default_factory=datetime.now)  # When the schedule was created
    attendance_marked: bool = field(default=False)      # Whether attendance was marked for this schedule

    # Table name in the database
    __tablename__ = 'schedules'

    @classmethod
    def create_table(cls):
        """Creates the schedules table if it doesn't exist."""
        query = f'''
        CREATE TABLE IF NOT EXISTS {cls.__tablename__} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            week_number INTEGER NOT NULL,
            dow TEXT NOT NULL,
            driver_id INTEGER NOT NULL,
            loader_ids TEXT,
            notification_sent BOOLEAN DEFAULT 0,
            schedule_created_at DATETIME NOT NULL,
            attendance_marked BOOLEAN DEFAULT 0
        )
        '''
        db.execute(query)

    @classmethod
    def find_all(cls) -> List['Schedule']:
        """Fetches all schedules from the database."""
        query = f"SELECT * FROM {cls.__tablename__} ORDER BY schedule_created_at DESC"
        rows = db.q(query)
        return [cls(**cls._parse_row(row)) for row in rows]

    @classmethod
    def find_by_id(cls, schedule_id: int) -> Optional['Schedule']:
        """Finds a schedule by ID."""
        query = f"SELECT * FROM {cls.__tablename__} WHERE id = ?"
        row = db.fetch_one(query, (schedule_id,))
        if row:
            return cls(**cls._parse_row(row))
        return None

    def save(self):
        """Inserts or updates the schedule in the database."""
        loader_ids_str = ",".join(map(str, self.loader_ids)) if self.loader_ids else ""
        if self.id is None:
            # Insert new schedule
            query = f'''
            INSERT INTO {self.__tablename__} (
                week_number, dow, driver_id, loader_ids, notification_sent, schedule_created_at, attendance_marked
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            '''
            params = (
                self.week_number, self.dow, self.driver_id, loader_ids_str,
                int(self.notification_sent),
                self.schedule_created_at.strftime("%Y-%m-%d %H:%M:%S"),
                int(self.attendance_marked)
            )
            self.id = db.insert(query, params)
        else:
            # Update existing schedule
            query = f'''
            UPDATE {self.__tablename__}
            SET week_number = ?, dow = ?, driver_id = ?, loader_ids = ?, notification_sent = ?, schedule_created_at = ?, attendance_marked = ?
            WHERE id = ?
            '''
            params = (
                self.week_number, self.dow, self.driver_id, loader_ids_str,
                int(self.notification_sent),
                self.schedule_created_at.strftime("%Y-%m-%d %H:%M:%S"),
                int(self.attendance_marked),
                self.id
            )
            db.execute(query, params)

    def delete(self):
        """Deletes the schedule from the database."""
        query = f"DELETE FROM {self.__tablename__} WHERE id = ?"
        db.execute(query, (self.id,))

    @staticmethod
    def _parse_row(row):
        """Parses a database row into a dictionary for initializing a Schedule object."""
        loader_ids = [int(id_str) for id_str in row['loader_ids'].split(",")] if row['loader_ids'] else []
        return {
            'id': row['id'],
            'week_number': row['week_number'],
            'dow': row['dow'],
            'driver_id': row['driver_id'],
            'loader_ids': loader_ids,
            'notification_sent': bool(row['notification_sent']),
            'schedule_created_at': datetime.strptime(row['schedule_created_at'], "%Y-%m-%d %H:%M:%S"),
            'attendance_marked': bool(row['attendance_marked'])
        }

    def __ft__(self):
        """Provides a FastHTML representation of the schedule."""
        from fasthtml.common import Li, Div, A
        return Li(
            Div(f"Schedule ID: {self.id}"),
            Div(f"Week Number: {self.week_number}"),
            Div(f"Day of Week: {self.dow}"),
            Div(f"Driver ID: {self.driver_id}"),
            Div(f"Loader IDs: {', '.join(map(str, self.loader_ids))}"),
            Div(f"Notification Sent: {'Yes' if self.notification_sent else 'No'}"),
            Div(f"Created At: {self.schedule_created_at.strftime('%Y-%m-%d %H:%M:%S')}"),
            Div(f"Attendance Marked: {'Yes' if self.attendance_marked else 'No'}"),
            Div(
                A("Edit", href=f"/schedules/edit/{self.id}"),
                " | ",
                A("Delete", href=f"/schedules/delete/{self.id}", hx_post=f"/schedules/delete/{self.id}",
                  hx_confirm="Are you sure?", hx_target="#schedule-list")
            )
        )


@dataclass
class ServiceSchedule:
    id: int = field(default=None)
    service_name: str = field(default="")                 # Name of the service
    schedule_time: datetime = field(default_factory=datetime.now)  # When the service is scheduled
    assigned_driver_id: int = field(default=None)         # Assigned Driver ID
    notification_sent: bool = field(default=False)        # Whether notifications have been sent

    # Table name in the database
    __tablename__ = 'service_schedules'

    @classmethod
    def create_table(cls):
        """Creates the service_schedules table if it doesn't exist."""
        query = f'''
        CREATE TABLE IF NOT EXISTS {cls.__tablename__} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service_name TEXT NOT NULL,
            schedule_time DATETIME NOT NULL,
            assigned_driver_id INTEGER,
            notification_sent BOOLEAN DEFAULT 0
        )
        '''
        db.execute(query)

    @classmethod
    def find_all(cls) -> List['ServiceSchedule']:
        """Fetches all service schedules from the database."""
        query = f"SELECT * FROM {cls.__tablename__} ORDER BY schedule_time DESC"
        rows = db.fetch_all(query)
        return [cls(**cls._parse_row(row)) for row in rows]

    @classmethod
    def find_by_id(cls, service_schedule_id: int) -> Optional['ServiceSchedule']:
        """Finds a service schedule by ID."""
        query = f"SELECT * FROM {cls.__tablename__} WHERE id = ?"
        row = db.fetch_one(query, (service_schedule_id,))
        if row:
            return cls(**cls._parse_row(row))
        return None

    def save(self):
        """Inserts or updates the service schedule in the database."""
        if self.id is None:
            # Insert new service schedule
            query = f'''
            INSERT INTO {self.__tablename__} (
                service_name, schedule_time, assigned_driver_id, notification_sent
            ) VALUES (?, ?, ?, ?)
            '''
            params = (
                self.service_name,
                self.schedule_time.strftime("%Y-%m-%d %H:%M:%S"),
                self.assigned_driver_id,
                int(self.notification_sent)
            )
            self.id = db.insert(query, params)
        else:
            # Update existing service schedule
            query = f'''
            UPDATE {self.__tablename__}
            SET service_name = ?, schedule_time = ?, assigned_driver_id = ?, notification_sent = ?
            WHERE id = ?
            '''
            params = (
                self.service_name,
                self.schedule_time.strftime("%Y-%m-%d %H:%M:%S"),
                self.assigned_driver_id,
                int(self.notification_sent),
                self.id
            )
            db.execute(query, params)

    def delete(self):
        """Deletes the service schedule from the database."""
        query = f"DELETE FROM {self.__tablename__} WHERE id = ?"
        db.execute(query, (self.id,))

    @staticmethod
    def _parse_row(row):
        """Parses a database row into a dictionary for initializing a ServiceSchedule object."""
        return {
            'id': row['id'],
            'service_name': row['service_name'],
            'schedule_time': datetime.strptime(row['schedule_time'], "%Y-%m-%d %H:%M:%S"),
            'assigned_driver_id': row['assigned_driver_id'],
            'notification_sent': bool(row['notification_sent'])
        }

    def __ft__(self):
        """Provides a FastHTML representation of the service schedule."""
        from fasthtml.common import Li, Div, A
        return Li(
            Div(f"Service Schedule ID: {self.id}"),
            Div(f"Service Name: {self.service_name}"),
            Div(f"Scheduled Time: {self.schedule_time.strftime('%Y-%m-%d %H:%M:%S')}"),
            Div(f"Assigned Driver ID: {self.assigned_driver_id}"),
            Div(f"Notification Sent: {'Yes' if self.notification_sent else 'No'}"),
            Div(
                A("Edit", href=f"/service-schedules/edit/{self.id}"),
                " | ",
                A("Delete", href=f"/service-schedules/delete/{self.id}", hx_post=f"/service-schedules/delete/{self.id}",
                  hx_confirm="Are you sure?", hx_target="#service-schedule-list")
            )
        )