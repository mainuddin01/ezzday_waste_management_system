# components/report/services.py

# services.py

import json
from app.components.report.models import Report
from datetime import datetime
import csv
import os
from typing import Optional
from fastlite import Database

db = Database('app_data.db')

def generate_report(report_type: str, parameters: Optional[dict] = None) -> Report:
    """
    Generates a report of the given type and stores it.
    Raises:
        ValueError: If validation fails.
    """
    report_data = []
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    file_name = f"{report_type.lower().replace(' ', '_')}_{timestamp}.csv"
    file_path = os.path.join('reports', file_name)

    # Ensure the reports directory exists
    os.makedirs('reports', exist_ok=True)

    # Fetch data based on report type
    if report_type == "End of Day":
        report_data = get_end_of_day_report(parameters)
    elif report_type == "Issue Report":
        report_data = get_issue_report(parameters)
    elif report_type == "Schedule Report":
        report_data = get_schedule_report(parameters)
    elif report_type == "Attendance Report":
        report_data = get_attendance_report(parameters)
    elif report_type == "Custom Report":
        report_data = get_custom_report(parameters)
    else:
        raise ValueError("Invalid report type.")

    # Write report data to CSV
    if report_data:
        with open(file_path, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            # Write headers
            writer.writerow(report_data[0].keys())
            # Write data
            for row in report_data:
                writer.writerow(row.values())
    else:
        raise ValueError("No data found for the given parameters.")

    # Save report metadata
    new_report = Report(
        report_type=report_type,
        parameters=parameters,
        generated_at=datetime.now(),
        file_path=file_path
    )
    new_report.save()
    return new_report

def get_end_of_day_report(parameters: dict):
    """Fetches data for the End of Day report."""
    date = parameters.get('date', datetime.now().strftime('%Y-%m-%d'))
    query = "SELECT * FROM assignments WHERE doc = ?"
    rows = db.fetch_all(query, (date,))
    return rows

def get_issue_report(parameters: dict):
    """Fetches data for the Issue Report."""
    start_date = parameters.get('start_date')
    end_date = parameters.get('end_date')
    if not start_date or not end_date:
        raise ValueError("Start date and end date are required for Issue Report.")
    query = "SELECT * FROM issues WHERE date_reported BETWEEN ? AND ?"
    rows = db.fetch_all(query, (start_date, end_date))
    return rows

def get_schedule_report(parameters: dict):
    """Fetches data for the Schedule Report."""
    week_number = parameters.get('week_number')
    if not week_number:
        raise ValueError("Week number is required for Schedule Report.")
    query = "SELECT * FROM schedules WHERE week_number = ?"
    rows = db.fetch_all(query, (week_number,))
    return rows

def get_attendance_report(parameters: dict):
    """Fetches data for the Attendance Report."""
    query = "SELECT * FROM schedules WHERE attendance_marked = 1"
    rows = db.fetch_all(query)
    return rows

def get_custom_report(parameters: dict):
    """Fetches data for a Custom Report based on a custom query."""
    query = parameters.get('query')
    if not query:
        raise ValueError("Custom query is required for Custom Report.")
    rows = db.fetch_all(query)
    return rows