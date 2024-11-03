# components/loader/services.py
# services.py

from app.components.loader.models import Loader
from typing import List

def get_all_loaders() -> List[Loader]:
    """Fetches all loaders."""
    return Loader.find_all()

def get_loader_by_id(loader_id: int) -> Loader:
    """Fetches a loader by its ID."""
    return Loader.find_by_id(loader_id)

def create_loader(data):
    """
    Creates a new loader.
    Raises:
        ValueError: If validation fails.
    """
    name = data.get('name')
    pickup_spot = data.get('pickup_spot')

    # Input Validation
    if not name or not pickup_spot:
        raise ValueError("Loader Name and Pickup Spot are required.")

    # Check for duplicate loader name
    if Loader.find_by_name(name):
        raise ValueError("A loader with this name already exists.")

    new_loader = Loader(
        name=name,
        pickup_spot=pickup_spot
    )
    new_loader.save()

def update_loader(loader_id: int, data):
    """
    Updates an existing loader.
    Raises:
        ValueError: If validation fails.
    """
    loader = get_loader_by_id(loader_id)
    if not loader:
        raise ValueError("Loader not found.")

    name = data.get('name')
    pickup_spot = data.get('pickup_spot')

    # Input Validation
    if not name or not pickup_spot:
        raise ValueError("Loader Name and Pickup Spot are required.")

    # Check for duplicate loader name
    existing_loader = Loader.find_by_name(name)
    if existing_loader and existing_loader.id != loader_id:
        raise ValueError("Another loader with this name already exists.")

    loader.name = name
    loader.pickup_spot = pickup_spot
    loader.save()

def delete_loader(loader_id: int):
    """Deletes an existing loader."""
    loader = get_loader_by_id(loader_id)
    if loader:
        loader.delete()