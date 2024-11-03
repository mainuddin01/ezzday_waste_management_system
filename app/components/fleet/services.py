# app/components/fleet/services.py

from app.components.fleet.models import Truck
from datetime import datetime
from typing import List

def get_all_trucks() -> List[Truck]:
    """Fetches all trucks."""
    return Truck.find_all()

def get_truck_by_id(truck_id: int) -> Truck:
    """Fetches a truck by its ID."""
    return Truck.find_by_id(truck_id)

def create_truck(data):
    """
    Creates a new truck.
    Raises:
        ValueError: If validation fails.
    """
    truck_number = data.get('truck_number')
    plate_number = data.get('plate_number')
    truck_type = data.get('truck_type')
    capacity = data.get('capacity')
    status = data.get('status')

    # Input Validation
    if not truck_number or not plate_number or not truck_type or not capacity or not status:
        raise ValueError("All required fields must be filled.")

    # Check for duplicate truck number or plate number
    if Truck.find_by_truck_number(truck_number):
        raise ValueError("A truck with this truck number already exists.")

    if Truck.find_by_plate_number(plate_number):
        raise ValueError("A truck with this plate number already exists.")

    # Parse numeric and date fields
    try:
        capacity = int(capacity)
        if capacity <= 0:
            raise ValueError("Capacity must be a positive integer.")
    except ValueError:
        raise ValueError("Invalid capacity value.")

    # Parse optional fields
    engine_hours = float(data.get('engine_hours', 0.0))
    mileage = int(data.get('mileage', 0))
    monthly_fuel_consumption = float(data.get('monthly_fuel_consumption', 0.0))
    fuel_efficiency = float(data.get('fuel_efficiency', 0.0))
    onboarding_date = parse_date(data.get('onboarding_date'))
    decommissioning_date = parse_date(data.get('decommissioning_date'))
    last_inspection_date = parse_date(data.get('last_inspection_date'))
    next_inspection_due = parse_date(data.get('next_inspection_due'))
    emission_test_due = parse_date(data.get('emission_test_due'))
    tire_change_due = parse_date(data.get('tire_change_due'))
    brake_check_due = parse_date(data.get('brake_check_due'))

    new_truck = Truck(
        truck_number=truck_number,
        plate_number=plate_number,
        truck_type=truck_type,
        capacity=capacity,
        status=status,
        engine_hours=engine_hours,
        mileage=mileage,
        monthly_fuel_consumption=monthly_fuel_consumption,
        fuel_efficiency=fuel_efficiency,
        onboarding_date=onboarding_date,
        decommissioning_date=decommissioning_date,
        last_inspection_date=last_inspection_date,
        next_inspection_due=next_inspection_due,
        emission_test_due=emission_test_due,
        tire_change_due=tire_change_due,
        brake_check_due=brake_check_due
    )
    new_truck.save()

def update_truck(truck_id: int, data):
    """
    Updates an existing truck.
    Raises:
        ValueError: If validation fails.
    """
    truck = get_truck_by_id(truck_id)
    if not truck:
        raise ValueError("Truck not found.")

    truck_number = data.get('truck_number')
    plate_number = data.get('plate_number')
    truck_type = data.get('truck_type')
    capacity = data.get('capacity')
    status = data.get('status')

    # Input Validation
    if not truck_number or not plate_number or not truck_type or not capacity or not status:
        raise ValueError("All required fields must be filled.")

    # Check for duplicate truck number or plate number
    existing_truck_number = Truck.find_by_truck_number(truck_number)
    if existing_truck_number and existing_truck_number.id != truck_id:
        raise ValueError("Another truck with this truck number already exists.")

    existing_plate_number = Truck.find_by_plate_number(plate_number)
    if existing_plate_number and existing_plate_number.id != truck_id:
        raise ValueError("Another truck with this plate number already exists.")

    # Parse numeric and date fields
    try:
        capacity = int(capacity)
        if capacity <= 0:
            raise ValueError("Capacity must be a positive integer.")
    except ValueError:
        raise ValueError("Invalid capacity value.")

    # Parse optional fields
    engine_hours = float(data.get('engine_hours', truck.engine_hours))
    mileage = int(data.get('mileage', truck.mileage))
    monthly_fuel_consumption = float(data.get('monthly_fuel_consumption', truck.monthly_fuel_consumption))
    fuel_efficiency = float(data.get('fuel_efficiency', truck.fuel_efficiency))
    onboarding_date = parse_date(data.get('onboarding_date', truck.onboarding_date))
    decommissioning_date = parse_date(data.get('decommissioning_date', truck.decommissioning_date))
    last_inspection_date = parse_date(data.get('last_inspection_date', truck.last_inspection_date))
    next_inspection_due = parse_date(data.get('next_inspection_due', truck.next_inspection_due))
    emission_test_due = parse_date(data.get('emission_test_due', truck.emission_test_due))
    tire_change_due = parse_date(data.get('tire_change_due', truck.tire_change_due))
    brake_check_due = parse_date(data.get('brake_check_due', truck.brake_check_due))

    # Update truck attributes
    truck.truck_number = truck_number
    truck.plate_number = plate_number
    truck.truck_type = truck_type
    truck.capacity = capacity
    truck.status = status
    truck.engine_hours = engine_hours
    truck.mileage = mileage
    truck.monthly_fuel_consumption = monthly_fuel_consumption
    truck.fuel_efficiency = fuel_efficiency
    truck.onboarding_date = onboarding_date
    truck.decommissioning_date = decommissioning_date
    truck.last_inspection_date = last_inspection_date
    truck.next_inspection_due = next_inspection_due
    truck.emission_test_due = emission_test_due
    truck.tire_change_due = tire_change_due
    truck.brake_check_due = brake_check_due
    truck.save()

def delete_truck(truck_id: int):
    """Deletes an existing truck."""
    truck = get_truck_by_id(truck_id)
    if truck:
        truck.delete()

def parse_date(date_str, default=None):
    """Parses a date string into a date object."""
    if date_str:
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError(f"Invalid date format for {date_str}. Expected YYYY-MM-DD.")
    return default