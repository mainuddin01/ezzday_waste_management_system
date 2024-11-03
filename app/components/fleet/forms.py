# components/fleet/forms.py

from fasthtml.common import *
from datetime import date

def truck_form(action_url, method="post", truck=None):
    """Generates a form for creating or editing a truck."""
    truck_types = [
        ("Heavy-duty Garbage Truck", "Heavy-duty Garbage Truck"),
        ("Light-duty Half-Ton Truck", "Light-duty Half-Ton Truck"),
        ("Heavy-duty Flatbed Truck", "Heavy-duty Flatbed Truck")
    ]

    status_options = [
        ("Operational", "Operational"),
        ("Out of Service", "Out of Service"),
        ("Maintenance Due", "Maintenance Due")
    ]

    return Form(
        Div(
            Label("Truck Number:", For="truck_number"),
            Input(
                name="truck_number",
                type="text",
                id="truck_number",
                value=truck.truck_number if truck else "",
                placeholder="Enter truck number",
                required=True
            )
        ),
        Div(
            Label("Plate Number:", For="plate_number"),
            Input(
                name="plate_number",
                type="text",
                id="plate_number",
                value=truck.plate_number if truck else "",
                placeholder="Enter plate number",
                required=True
            )
        ),
        Div(
            Label("Truck Type:", For="truck_type"),
            Select(
                *[Option(label, value=value, selected=truck and truck.truck_type == value) for value, label in truck_types],
                name="truck_type",
                id="truck_type",
                required=True
            )
        ),
        Div(
            Label("Capacity (kg):", For="capacity"),
            Input(
                name="capacity",
                type="number",
                id="capacity",
                value=truck.capacity if truck else "",
                placeholder="Enter capacity",
                min="0",
                required=True
            )
        ),
        Div(
            Label("Status:", For="status"),
            Select(
                *[Option(label, value=value, selected=truck and truck.status == value) for value, label in status_options],
                name="status",
                id="status",
                required=True
            )
        ),
        Div(
            Label("Engine Hours:", For="engine_hours"),
            Input(
                name="engine_hours",
                type="number",
                id="engine_hours",
                value=truck.engine_hours if truck else "",
                placeholder="Enter engine hours",
                min="0",
                step="0.1"
            )
        ),
        Div(
            Label("Mileage (km):", For="mileage"),
            Input(
                name="mileage",
                type="number",
                id="mileage",
                value=truck.mileage if truck else "",
                placeholder="Enter mileage",
                min="0"
            )
        ),
        Div(
            Label("Monthly Fuel Consumption (L):", For="monthly_fuel_consumption"),
            Input(
                name="monthly_fuel_consumption",
                type="number",
                id="monthly_fuel_consumption",
                value=truck.monthly_fuel_consumption if truck else "",
                placeholder="Enter monthly fuel consumption",
                min="0",
                step="0.1"
            )
        ),
        Div(
            Label("Fuel Efficiency (km/L):", For="fuel_efficiency"),
            Input(
                name="fuel_efficiency",
                type="number",
                id="fuel_efficiency",
                value=truck.fuel_efficiency if truck else "",
                placeholder="Enter fuel efficiency",
                min="0",
                step="0.1"
            )
        ),
        Div(
            Label("Onboarding Date:", For="onboarding_date"),
            Input(
                name="onboarding_date",
                type="date",
                id="onboarding_date",
                value=truck.onboarding_date if truck and truck.onboarding_date else "",
                max=str(date.today())
            )
        ),
        Div(
            Label("Decommissioning Date:", For="decommissioning_date"),
            Input(
                name="decommissioning_date",
                type="date",
                id="decommissioning_date",
                value=truck.decommissioning_date if truck and truck.decommissioning_date else "",
                min=str(date.today())
            )
        ),
        Div(
            Label("Last Inspection Date:", For="last_inspection_date"),
            Input(
                name="last_inspection_date",
                type="date",
                id="last_inspection_date",
                value=truck.last_inspection_date if truck and truck.last_inspection_date else "",
                max=str(date.today())
            )
        ),
        Div(
            Label("Next Inspection Due:", For="next_inspection_due"),
            Input(
                name="next_inspection_due",
                type="date",
                id="next_inspection_due",
                value=truck.next_inspection_due if truck and truck.next_inspection_due else "",
                min=str(date.today())
            )
        ),
        Div(
            Label("Emission Test Due:", For="emission_test_due"),
            Input(
                name="emission_test_due",
                type="date",
                id="emission_test_due",
                value=truck.emission_test_due if truck and truck.emission_test_due else "",
                min=str(date.today())
            )
        ),
        Div(
            Label("Tire Change Due:", For="tire_change_due"),
            Input(
                name="tire_change_due",
                type="date",
                id="tire_change_due",
                value=truck.tire_change_due if truck and truck.tire_change_due else "",
                min=str(date.today())
            )
        ),
        Div(
            Label("Brake Check Due:", For="brake_check_due"),
            Input(
                name="brake_check_due",
                type="date",
                id="brake_check_due",
                value=truck.brake_check_due if truck and truck.brake_check_due else "",
                min=str(date.today())
            )
        ),
        Button("Submit", type="submit"),
        action=action_url,
        method=method
    )