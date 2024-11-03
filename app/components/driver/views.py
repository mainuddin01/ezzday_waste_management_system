# components/driver/views.py

from fasthtml.common import *
from app.components.driver.forms import driver_form
from app.components.driver.services import (
    get_all_drivers, get_driver_by_id, create_driver, update_driver, delete_driver
)
from app.components.common.page import page_view
from starlette.responses import RedirectResponse
from starlette.requests import Request
import logging

logger = logging.getLogger(__name__)

async def driver_list_view(req: Request):
    """Generates the driver list view."""
    drivers = get_all_drivers()
    content = [
        H1("Drivers"),
        Table(
            Thead(
                Tr(
                    Th("ID"), Th("Name"), Th("License Number"), Th("Actions")
                )
            ),
            Tbody(
                *[
                    Tr(
                        Td(str(driver.id)),
                        Td(driver.name),
                        Td(driver.license_number),
                        Td(
                            A("Edit", href=f"/drivers/edit/{driver.id}", cls="button small"),
                            " ",
                            A("Delete", href=f"/drivers/delete/{driver.id}", cls="button small danger")
                        )
                    ) for driver in drivers
                ]
            ),
            cls="table-responsive"
        ),
        A("Add New Driver", href="/drivers/add", cls="button")
    ]
    return page_view(req, "Driver List", content)

async def driver_add_view(req: Request):
    """Handles adding a new driver."""
    if req.method == "GET":
        content = [
            driver_form("/drivers/add")
        ]
        return page_view(req, "Add Driver", content)
    elif req.method == "POST":
        data = await req.form()
        try:
            create_driver(data)
            return RedirectResponse("/drivers", status_code=303)
        except ValueError as e:
            logger.error(f"Error creating driver: {e}")
            content = [
                P(str(e), style="color:red"),
                driver_form("/drivers/add")
            ]
            return page_view(req, "Add Driver", content)

async def driver_edit_view(req: Request, driver_id: int):
    """Handles editing an existing driver."""
    driver = get_driver_by_id(driver_id)
    if not driver:
        return page_view(req, "Error", [Div("Driver not found.")])

    if req.method == "GET":
        content = [
            driver_form(f"/drivers/edit/{driver_id}", driver=driver)
        ]
        return page_view(req, "Edit Driver", content)
    elif req.method == "POST":
        data = await req.form()
        try:
            update_driver(driver_id, data)
            return RedirectResponse("/drivers", status_code=303)
        except ValueError as e:
            logger.error(f"Error updating driver: {e}")
            content = [
                P(str(e), style="color:red"),
                driver_form(f"/drivers/edit/{driver_id}", driver=driver)
            ]
            return page_view(req, "Edit Driver", content)

async def driver_delete_view(req: Request, driver_id: int):
    """Handles deleting an existing driver."""
    driver = get_driver_by_id(driver_id)
    if not driver:
        return page_view(req, "Error", [Div("Driver not found.")])

    if req.method == "POST":
        delete_driver(driver_id)
        return RedirectResponse("/drivers", status_code=303)
    else:
        content = [
            H2(f"Are you sure you want to delete driver {driver.name}?"),
            Form(
                Button("Yes, delete", type="submit", cls="button danger"),
                action=f"/drivers/delete/{driver_id}",
                method="post"
            )
        ]
        return page_view(req, "Delete Driver", content)