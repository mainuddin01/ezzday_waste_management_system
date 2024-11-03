# real_time_service.py

import asyncio
import json
import logging
from datetime import datetime, date
from typing import List

from fastlite import Database
from starlette.websockets import WebSocket, WebSocketDisconnect
from email.mime.text import MIMEText

from app.components.assignment.models import Assignment
from app.components.supervisor.models import Supervisor
from app.components.dispatch.models import Dispatch
from app.components.notification.services import send_email_async, send_sms_async

logger = logging.getLogger(__name__)

# Initialize the FastLite database
db = Database('app_data.db')


async def send_sms(phone_number: str, message: str):
    """
    Sends an SMS message asynchronously.
    Integrate with an SMS provider (e.g., Twilio) for actual SMS sending.
    """
    # Implement SMS sending logic here
    # For demonstration purposes, we log the message
    logger.info(f"Sending SMS to {phone_number}: {message}")
    # Example with Twilio (uncomment and configure):
    # from twilio.rest import Client
    # client = Client(account_sid, auth_token)
    # message = client.messages.create(
    #     body=message,
    #     from_='+1234567890',
    #     to=phone_number
    # )


async def notify_repeat_offenders(address_list: List[str]):
    """
    Notify supervisors or admins about repeat offender addresses.
    """
    subject = "Repeat Offender Notification"
    supervisors = Supervisor.find_all()
    for address in address_list:
        message = f"The address {address} has been marked as a repeat offender."
        for supervisor in supervisors:
            await send_email_async(supervisor.email, subject, message)
            # Optionally, send SMS alerts as well
            # if supervisor.phone_number:
            #     await send_sms(supervisor.phone_number, message)


async def track_route_progress(websocket: WebSocket):
    """
    Track route progress in real-time, providing updates and handling alerts.
    """
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            try:
                data_dict = json.loads(data)
                route_id = data_dict.get('route_id')
                location = data_dict.get('location')
                status = data_dict.get('status')  # e.g., "On Track", "Delayed", "Issue"

                # Handle different statuses for alerts
                if status == "Delayed":
                    await handle_delayed_route(route_id, location)
                elif status == "Issue":
                    await handle_issue_reported(route_id, location)

                # Send a response back to confirm receipt
                await websocket.send_text(
                    f"Update received for Route {route_id}: Status - {status}, Location - {location}"
                )

            except json.JSONDecodeError:
                logger.error("Invalid JSON received from WebSocket.")
                await websocket.send_text("Error: Invalid data format. Please send JSON.")

    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")


async def handle_delayed_route(route_id: int, location: str):
    """
    Handle scenarios where a route is reported as delayed.
    Send alerts to dispatch and supervisors.
    """
    subject = f"Route {route_id} Delayed Alert"
    message = (
        f"Route {route_id} has been reported as delayed at location: {location}. "
        "Please investigate."
    )

    supervisors = Supervisor.find_all()
    for supervisor in supervisors:
        await send_email_async(supervisor.email, subject, message)
        # Optionally, send SMS alerts as well
        # if supervisor.phone_number:
        #     await send_sms(supervisor.phone_number, message)


async def handle_issue_reported(route_id: int, location: str):
    """
    Handle scenarios where an issue is reported during the route collection.
    Send alerts and ensure the issue is logged.
    """
    subject = f"Issue Reported on Route {route_id}"
    message = (
        f"An issue has been reported on Route {route_id} at location: {location}. "
        "Please review and take necessary actions."
    )

    supervisors = Supervisor.find_all()
    for supervisor in supervisors:
        await send_email_async(supervisor.email, subject, message)
        # Optionally, send SMS alerts as well
        # if supervisor.phone_number:
        #     await send_sms(supervisor.phone_number, message)

    # Log the issue in the database (optional)
    log_issue(route_id, location, message)


def log_issue(route_id: int, location: str, description: str):
    """
    Logs an issue in the database.
    """
    query = '''
    INSERT INTO issues (route_id, location, description, date_reported)
    VALUES (?, ?, ?, ?)
    '''
    params = (route_id, location, description, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    db.execute(query, params)
    logger.info(f"Issue logged for Route {route_id} at {location}")


async def notify_attendance_ppe_missing(assignment_id: int, crew_id: int):
    """
    Notify supervisors if attendance or PPE compliance is missing by the 8 AM deadline.
    """
    subject = "Attendance/PPE Compliance Missing"
    message = (
        f"Crew ID: {crew_id} for Assignment ID: {assignment_id} has not confirmed attendance "
        "or PPE compliance by 8 AM. Please follow up immediately."
    )

    supervisors = Supervisor.find_all()
    for supervisor in supervisors:
        await send_email_async(supervisor.email, subject, message)
        # Optionally, send SMS alerts as well
        # if supervisor.phone_number:
        #     await send_sms(supervisor.phone_number, message)


async def periodic_alert_checker():
    """
    Periodically check all assignments to ensure updates are being provided at key points.
    """
    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        check_times = {
            "11:00": "11AM",
            "13:00": "1PM",
            "15:00": "3PM",
            "18:00": "EOD"
        }

        if current_time in check_times:
            time_label = check_times[current_time]
            assignments = Assignment.find_all_for_date(date.today())
            for assignment in assignments:
                if assignment.status_updates.get(time_label) is None:
                    alert_message = (
                        f"Status update missing for Crew ID: {assignment.crew_id} on Assignment ID: {assignment.id} "
                        f"at checkpoint: {time_label}. Please follow up."
                    )
                    supervisors = Supervisor.find_all()
                    for supervisor in supervisors:
                        await send_email_async(supervisor.email, "Status Update Missing", alert_message)
                        # Optionally, send SMS alerts as well
                        # if supervisor.phone_number:
                        #     await send_sms(supervisor.phone_number, alert_message)

        # Check for attendance and PPE compliance at 8 AM
        if current_time == "08:00":
            await check_attendance_ppe_compliance()

        # Wait for the next minute before checking again
        await asyncio.sleep(60)


async def check_attendance_ppe_compliance():
    """
    Checks attendance and PPE compliance for all assignments at 8 AM.
    """
    assignments = Assignment.find_all_for_date(date.today())
    for assignment in assignments:
        if not assignment.attendance_confirmed or not assignment.ppe_compliant:
            await notify_attendance_ppe_missing(assignment.id, assignment.crew_id)


def start_dispatch_alerts():
    """
    Start the periodic alert system for dispatch.
    Run the periodic alert checker as a background task.
    """
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(periodic_alert_checker())
    loop.run_forever()