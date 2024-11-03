# components/schedule/services.py
# services.py

from app.components.schedule.models import Schedule
from app.components.driver.models import Driver
from app.components.loader.models import Loader
from app.components.driver.services import get_driver_by_id
from app.components.loader.services import get_loader_by_id
from datetime import datetime
from typing import List
import smtplib
from email.mime.text import MIMEText
import logging

logger = logging.getLogger(__name__)

def send_notification(email: str, subject: str, message: str):
    """Utility function to send email notifications."""
    try:
        smtp = smtplib.SMTP('smtp.example.com')
        smtp.starttls()
        smtp.login('username', 'password')
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = 'no-reply@example.com'
        msg['To'] = email
        smtp.sendmail('no-reply@example.com', [email], msg.as_string())
        smtp.quit()
        logger.info(f"Email sent to {email}")
    except Exception as e:
        logger.error(f"Failed to send email to {email}: {e}")

def create_schedule(data):
    """
    Creates a new schedule and sends notifications to assigned crew.
    Raises:
        ValueError: If validation fails.
    """
    try:
        week_number = int(data['week_number'])
        dow = data['dow']
        driver_id = int(data['driver_id'])
        loader_ids = [int(id_) for id_ in data.getlist('loader_ids')]

        # Input Validation
        if not dow or not driver_id:
            raise ValueError("Day of Week and Driver are required.")

        # Check for valid driver
        driver = get_driver_by_id(driver_id)
        if not driver:
            raise ValueError("Invalid driver selected.")

        # Check for valid loaders
        loaders = []
        for loader_id in loader_ids:
            loader = get_loader_by_id(loader_id)
            if not loader:
                raise ValueError(f"Invalid loader selected: {loader_id}")
            loaders.append(loader)

        # Create the schedule
        new_schedule = Schedule(
            week_number=week_number,
            dow=dow,
            driver_id=driver_id,
            loader_ids=loader_ids,
            schedule_created_at=datetime.now()
        )
        new_schedule.save()

        # Send notifications
        send_schedule_notifications(new_schedule, driver, loaders)

        # Update schedule to indicate notifications have been sent
        new_schedule.notification_sent = True
        new_schedule.save()
    except (ValueError, KeyError) as e:
        raise ValueError(f"Error creating schedule: {e}") from e

def send_schedule_notifications(schedule: Schedule, driver: Driver, loaders: List[Loader]):
    """Sends schedule notifications to the driver and loaders."""
    subject = f"Your Work Schedule for Week {schedule.week_number}"
    message = f"You are scheduled to work on {schedule.dow} in week {schedule.week_number}."

    # Send email to driver
    if driver.email:
        send_notification(driver.email, subject, message)
    else:
        logger.warning(f"Driver {driver.id} does not have an email address.")

    # Send emails to loaders
    for loader in loaders:
        if loader.email:
            send_notification(loader.email, subject, message)
        else:
            logger.warning(f"Loader {loader.id} does not have an email address.")

def update_schedule(schedule_id: int, data):
    """
    Updates an existing schedule.
    Raises:
        ValueError: If validation fails.
    """
    schedule = Schedule.find_by_id(schedule_id)
    if not schedule:
        raise ValueError("Schedule not found.")

    try:
        week_number = int(data['week_number'])
        dow = data['dow']
        driver_id = int(data['driver_id'])
        loader_ids = [int(id_) for id_ in data.getlist('loader_ids')]

        # Input Validation
        if not dow or not driver_id:
            raise ValueError("Day of Week and Driver are required.")

        # Update schedule
        schedule.week_number = week_number
        schedule.dow = dow
        schedule.driver_id = driver_id
        schedule.loader_ids = loader_ids
        schedule.save()
    except (ValueError, KeyError) as e:
        raise ValueError(f"Error updating schedule: {e}") from e

def delete_schedule(schedule_id: int):
    """Deletes an existing schedule."""
    schedule = Schedule.find_by_id(schedule_id)
    if schedule:
        schedule.delete()