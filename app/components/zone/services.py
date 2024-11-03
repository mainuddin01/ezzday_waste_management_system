# components/zone/services.py

from typing import List, Optional
from app.components.zone.models import Zone

def get_all_zones() -> List[Zone]:
    """Fetches all zones."""
    return Zone.find_all()

def get_zone_by_id(zone_id: int) -> Optional[Zone]:
    """Fetches a zone by its ID."""
    return Zone.find_by_id(zone_id)

def create_zone(data):
    """
    Creates a new zone.
    Raises:
        ValueError: If validation fails.
    """
    name = data.get('name')
    client_id = data.get('client_id')
    description = data.get('description', '')

    # Input Validation
    if not name or not client_id:
        raise ValueError("Zone Name and Client are required.")

    # Check for valid client
    from app.components.client.services import get_client_by_id  # Import inside function
    client = get_client_by_id(int(client_id))
    if not client:
        raise ValueError("Invalid client selected.")

    # Check for duplicate zone name within the client
    if Zone.find_by_name_and_client(name, int(client_id)):
        raise ValueError("A zone with this name already exists for the selected client.")

    new_zone = Zone(
        name=name,
        client_id=int(client_id),
        description=description
    )
    new_zone.save()

def update_zone(zone_id: int, data):
    """
    Updates an existing zone.
    Raises:
        ValueError: If validation fails.
    """
    zone = get_zone_by_id(zone_id)
    if not zone:
        raise ValueError("Zone not found.")

    name = data.get('name')
    client_id = data.get('client_id')
    description = data.get('description', '')

    # Input Validation
    if not name or not client_id:
        raise ValueError("Zone Name and Client are required.")

    # Check for valid client
    from app.components.client.services import get_client_by_id  # Import inside function
    client = get_client_by_id(int(client_id))
    if not client:
        raise ValueError("Invalid client selected.")

    # Check for duplicate zone name within the client
    existing_zone = Zone.find_by_name_and_client(name, int(client_id))
    if existing_zone and existing_zone.id != zone_id:
        raise ValueError("Another zone with this name already exists for the selected client.")

    zone.name = name
    zone.client_id = int(client_id)
    zone.description = description
    zone.save()

def delete_zone(zone_id: int):
    """Deletes an existing zone."""
    zone = get_zone_by_id(zone_id)
    if zone:
        zone.delete()