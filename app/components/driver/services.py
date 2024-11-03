# components/driver/services.py

from app.components.driver.models import Driver
from datetime import datetime
from typing import List

def get_all_drivers() -> List[Driver]:
    """Fetches all drivers."""
    return Driver.find_all()

def get_driver_by_id(driver_id: int) -> Driver:
    """Fetches a driver by its ID."""
    return Driver.find_by_id(driver_id)

def create_driver(data):
    """
    Creates a new driver.
    Raises:
        ValueError: If validation fails.
    """
    name = data.get('name')
    license_number = data.get('license_number')
    license_expiry = data.get('license_expiry')
    last_medical_check = data.get('last_medical_check', None)

    # Input Validation
    if not name or not license_number or not license_expiry:
        raise ValueError("Name, License Number, and License Expiry are required.")

    # Check for duplicate license number
    if Driver.find_by_license_number(license_number):
        raise ValueError("A driver with this license number already exists.")

    # Date Validation
    try:
        license_expiry_date = datetime.strptime(license_expiry, "%Y-%m-%d").date()
        if license_expiry_date < datetime.today().date():
            raise ValueError("License expiry date cannot be in the past.")
    except ValueError:
        raise ValueError("Invalid license expiry date format.")

    if last_medical_check:
        try:
            last_medical_check_date = datetime.strptime(last_medical_check, "%Y-%m-%d").date()
            if last_medical_check_date > datetime.today().date():
                raise ValueError("Last medical check date cannot be in the future.")
        except ValueError:
            raise ValueError("Invalid last medical check date format.")
    else:
        last_medical_check_date = None

    new_driver = Driver(
        name=name,
        license_number=license_number,
        license_expiry=license_expiry_date,
        last_medical_check=last_medical_check_date
    )
    new_driver.save()

def update_driver(driver_id: int, data):
    """
    Updates an existing driver.
    Raises:
        ValueError: If validation fails.
    """
    driver = get_driver_by_id(driver_id)
    if not driver:
        raise ValueError("Driver not found.")

    name = data.get('name')
    license_number = data.get('license_number')
    license_expiry = data.get('license_expiry')
    last_medical_check = data.get('last_medical_check', None)

    # Input Validation
    if not name or not license_number or not license_expiry:
        raise ValueError("Name, License Number, and License Expiry are required.")

    # Check for duplicate license number
    existing_driver = Driver.find_by_license_number(license_number)
    if existing_driver and existing_driver.id != driver_id:
        raise ValueError("Another driver with this license number already exists.")

    # Date Validation
    try:
        license_expiry_date = datetime.strptime(license_expiry, "%Y-%m-%d").date()
        if license_expiry_date < datetime.today().date():
            raise ValueError("License expiry date cannot be in the past.")
    except ValueError:
        raise ValueError("Invalid license expiry date format.")

    if last_medical_check:
        try:
            last_medical_check_date = datetime.strptime(last_medical_check, "%Y-%m-%d").date()
            if last_medical_check_date > datetime.today().date():
                raise ValueError("Last medical check date cannot be in the future.")
        except ValueError:
            raise ValueError("Invalid last medical check date format.")
    else:
        last_medical_check_date = None

    driver.name = name
    driver.license_number = license_number
    driver.license_expiry = license_expiry_date
    driver.last_medical_check = last_medical_check_date
    driver.save()

def delete_driver(driver_id: int):
    """Deletes an existing driver."""
    driver = get_driver_by_id(driver_id)
    if driver:
        driver.delete()