# app/components/route/services.py

from typing import List, Optional
from app.components.route.models import Route

def get_all_routes() -> List[Route]:
    """Fetches all routes."""
    return Route.find_all()

def get_routes_by_zone_id(zone_id: int) -> List[Route]:
    """Fetches all routes related to a specific zone."""
    return Route.find_all_by_zone_id(zone_id)

def get_route_by_id(route_id: int) -> Optional[Route]:
    """Fetches a route by its ID."""
    return Route.find_by_id(route_id)

def create_route(data):
    """
    Creates a new route.
    Raises:
        ValueError: If validation fails.
    """
    name = data.get('name')
    zone_id = data.get('zone_id')
    description = data.get('description', '')

    # Input Validation
    if not name or not zone_id:
        raise ValueError("Route Name and Zone are required.")

    # Check for valid zone
    from app.components.zone.services import get_zone_by_id  # Import inside function
    zone = get_zone_by_id(int(zone_id))
    if not zone:
        raise ValueError("Invalid zone selected.")

    # Check for duplicate route name within the zone
    if Route.find_by_name_and_zone(name, int(zone_id)):
        raise ValueError("A route with this name already exists in the selected zone.")

    new_route = Route(
        name=name,
        zone_id=int(zone_id),
        description=description
    )
    new_route.save()

def update_route(route_id: int, data):
    """
    Updates an existing route.
    Raises:
        ValueError: If validation fails.
    """
    route = get_route_by_id(route_id)
    if not route:
        raise ValueError("Route not found.")

    name = data.get('name')
    zone_id = data.get('zone_id')
    description = data.get('description', '')

    # Input Validation
    if not name or not zone_id:
        raise ValueError("Route Name and Zone are required.")

    # Check for valid zone
    from app.components.zone.services import get_zone_by_id  # Import inside function
    zone = get_zone_by_id(int(zone_id))
    if not zone:
        raise ValueError("Invalid zone selected.")

    # Check for duplicate route name within the zone
    existing_route = Route.find_by_name_and_zone(name, int(zone_id))
    if existing_route and existing_route.id != route_id:
        raise ValueError("Another route with this name already exists in the selected zone.")

    route.name = name
    route.zone_id = int(zone_id)
    route.description = description
    route.save()

def delete_route(route_id: int):
    """Deletes an existing route."""
    route = get_route_by_id(route_id)
    if route:
        route.delete()