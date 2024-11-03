# components/event/services.py

from app.components.event.models import Event
from datetime import datetime
from typing import List

def get_all_events() -> List[Event]:
    """Fetches all events."""
    return Event.find_all()

def get_event_by_id(event_id: int) -> Event:
    """Fetches an event by its ID."""
    return Event.find_by_id(event_id)

def create_event(data):
    """
    Creates a new event.
    Raises:
        ValueError: If validation fails.
    """
    name = data.get('name')
    description = data.get('description', "")
    event_type = data.get('event_type')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    affected_clients = data.getlist('affected_clients')
    additional_info = data.get('additional_info', "")

    # Input Validation
    if not name or not event_type or not start_date or not end_date:
        raise ValueError("Event Name, Event Type, Start Date, and End Date are required.")

    # Date Validation
    try:
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()
        if start_date_obj > end_date_obj:
            raise ValueError("Start Date cannot be after End Date.")
    except ValueError:
        raise ValueError("Invalid date format.")

    affected_clients_list = list(map(int, affected_clients)) if affected_clients else []

    new_event = Event(
        name=name,
        description=description,
        start_date=start_date_obj,
        end_date=end_date_obj,
        affected_clients=affected_clients_list,
        event_type=event_type,
        additional_info=additional_info
    )
    new_event.save()

def update_event(event_id: int, data):
    """
    Updates an existing event.
    Raises:
        ValueError: If validation fails.
    """
    event = get_event_by_id(event_id)
    if not event:
        raise ValueError("Event not found.")

    name = data.get('name')
    description = data.get('description', "")
    event_type = data.get('event_type')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    affected_clients = data.getlist('affected_clients')
    additional_info = data.get('additional_info', "")

    # Input Validation
    if not name or not event_type or not start_date or not end_date:
        raise ValueError("Event Name, Event Type, Start Date, and End Date are required.")

    # Date Validation
    try:
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()
        if start_date_obj > end_date_obj:
            raise ValueError("Start Date cannot be after End Date.")
    except ValueError:
        raise ValueError("Invalid date format.")

    affected_clients_list = list(map(int, affected_clients)) if affected_clients else []

    event.name = name
    event.description = description
    event.start_date = start_date_obj
    event.end_date = end_date_obj
    event.affected_clients = affected_clients_list
    event.event_type = event_type
    event.additional_info = additional_info
    event.save()

def delete_event(event_id: int):
    """Deletes an existing event."""
    event = get_event_by_id(event_id)
    if event:
        event.delete()