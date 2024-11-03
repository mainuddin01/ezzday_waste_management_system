# components/fleet/views.py

from fasthtml.common import *
from app.components.fleet.forms import truck_form
from app.components.fleet.services import (
    get_all_trucks, get_truck_by_id, create_truck, update_truck, delete_truck
)
from app.components.common.page import page_view
from starlette.responses import RedirectResponse
from starlette.requests import Request
import logging

logger = logging.getLogger(__name__)

async def fleet_list_view(req: Request):
    """Generates the fleet list view."""
    trucks = get_all_trucks()
    content = [
        H1("Fleet Status"),
        Table(
            Thead(
                Tr(
                    Th("Truck Number"), Th("Plate Number"), Th("Type"), Th("Status"), Th("Actions")
                )
            ),
            Tbody(
                *[
                    Tr(
                        Td(truck.truck_number),
                        Td(truck.plate_number),
                        Td(truck.truck_type),
                        Td(truck.status),
                        Td(
                            A("View", href=f"/fleet/view/{truck.id}", cls="button small"),
                            " ",
                            A("Edit", href=f"/fleet/edit/{truck.id}", cls="button small"),
                            " ",
                            A("Delete", href=f"/fleet/delete/{truck.id}", cls="button small danger")
                        )
                    ) for truck in trucks
                ]
            ),
            cls="table-responsive"
        ),
        A("Add New Truck", href="/fleet/add", cls="button")
    ]
    return page_view(req, "Fleet Status", content)

async def fleet_add_view(req: Request):
    """Handles adding a new truck."""
    if req.method == "GET":
        content = [
            truck_form("/fleet/add")
        ]
        return page_view(req, "Add Truck", content)
    elif req.method == "POST":
        data = await req.form()
        try:
            create_truck(data)
            return RedirectResponse("/fleet", status_code=303)
        except ValueError as e:
            logger.error(f"Error creating truck: {e}")
            content = [
                P(str(e), style="color:red"),
                truck_form("/fleet/add")
            ]
            return page_view(req, "Add Truck", content)

async def fleet_edit_view(req: Request, truck_id: int):
    """Handles editing an existing truck."""
    truck = get_truck_by_id(truck_id)
    if not truck:
        return page_view(req, "Error", [Div("Truck not found.")])
    if req.method == "GET":
        content = [
            truck_form(f"/fleet/edit/{truck_id}", truck=truck)
        ]
        return page_view(req, "Edit Truck", content)
    elif req.method == "POST":
        data = await req.form()
        try:
            update_truck(truck_id, data)
            return RedirectResponse("/fleet", status_code=303)
        except ValueError as e:
            logger.error(f"Error updating truck: {e}")
            content = [
                P(str(e), style="color:red"),
                truck_form(f"/fleet/edit/{truck_id}", truck=truck)
            ]
            return page_view(req, "Edit Truck", content)

async def fleet_delete_view(req: Request, truck_id: int):
    """Handles deleting an existing truck."""
    truck = get_truck_by_id(truck_id)
    if not truck:
        return page_view(req, "Error", [Div("Truck not found.")])
    if req.method == "POST":
        delete_truck(truck_id)
        return RedirectResponse("/fleet", status_code=303)
    else:
        content = [
            H2(f"Are you sure you want to delete truck {truck.truck_number}?"),
            Form(
                Button("Yes, delete", type="submit", cls="button danger"),
                action=f"/fleet/delete/{truck_id}",
                method="post"
            )
        ]
        return page_view(req, "Delete Truck", content)

async def fleet_view(req: Request, truck_id: int):
    """Displays detailed information about a truck."""
    truck = get_truck_by_id(truck_id)
    if not truck:
        return page_view(req, "Error", [Div("Truck not found.")])
    content = [
        H1(f"Truck Number: {truck.truck_number}"),
        P(f"Plate Number: {truck.plate_number}"),
        P(f"Truck Type: {truck.truck_type}"),
        P(f"Capacity: {truck.capacity} kg"),
        P(f"Status: {truck.status}"),
        P(f"Engine Hours: {truck.engine_hours} hours"),
        P(f"Mileage: {truck.mileage} km"),
        P(f"Monthly Fuel Consumption: {truck.monthly_fuel_consumption} L"),
        P(f"Fuel Efficiency: {truck.fuel_efficiency} km/L"),
        P(f"Onboarding Date: {truck.onboarding_date}"),
        P(f"Decommissioning Date: {truck.decommissioning_date}" if truck.decommissioning_date else "Still operational"),
        P(f"Last Inspection Date: {truck.last_inspection_date}"),
        P(f"Next Inspection Due: {truck.next_inspection_due}"),
        P(f"Emission Test Due: {truck.emission_test_due}"),
        P(f"Tire Change Due: {truck.tire_change_due}"),
        P(f"Brake Check Due: {truck.brake_check_due}"),
        A("Edit Truck", href=f"/fleet/edit/{truck.id}", cls="button"),
        A("Delete Truck", href=f"/fleet/delete/{truck.id}", cls="button danger")
    ]
    return page_view(req, f"Truck {truck.truck_number}", content)