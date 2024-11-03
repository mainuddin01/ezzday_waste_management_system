# components/zone/views.py

from fasthtml.common import *
from app.components.zone.forms import zone_form
from app.components.zone.services import (
    get_all_zones, get_zone_by_id, create_zone, update_zone, delete_zone
)
from app.components.common.page import page_view
from starlette.responses import RedirectResponse
from starlette.requests import Request
import logging

logger = logging.getLogger(__name__)

async def zone_list_view(req: Request):
    """Generates the zone list view."""
    zones = get_all_zones()
    content = [
        H1("Zones"),
        Table(
            Thead(
                Tr(
                    Th("ID"), Th("Name"), Th("Description"), Th("Actions")
                )
            ),
            Tbody(
                *[
                    Tr(
                        Td(str(zone.id)),
                        Td(zone.name),
                        Td(zone.description),
                        Td(
                            A("View Routes", href=f"/zones/{zone.id}/routes", cls="button small"),
                            " ",
                            A("Edit", href=f"/zones/edit/{zone.id}", cls="button small"),
                            " ",
                            A("Delete", href=f"/zones/delete/{zone.id}", cls="button small danger")
                        )
                    ) for zone in zones
                ]
            ),
            cls="table-responsive"
        ),
        A("Add New Zone", href="/zones/add", cls="button")
    ]
    return page_view(req, "Zone List", content)

async def zone_add_view(req: Request):
    """Handles adding a new zone."""
    if req.method == "GET":
        content = [
            zone_form("/zones/add")
        ]
        return page_view(req, "Add Zone", content)
    elif req.method == "POST":
        data = await req.form()
        try:
            create_zone(data)
            return RedirectResponse("/zones", status_code=303)
        except ValueError as e:
            logger.error(f"Error creating zone: {e}")
            content = [
                P(str(e), style="color:red"),
                zone_form("/zones/add")
            ]
            return page_view(req, "Add Zone", content)

async def zone_edit_view(req: Request, zone_id: int):
    """Handles editing an existing zone."""
    zone = get_zone_by_id(zone_id)
    if not zone:
        return page_view(req, "Error", [Div("Zone not found.")])
    if req.method == "GET":
        content = [
            zone_form(f"/zones/edit/{zone_id}", zone=zone)
        ]
        return page_view(req, "Edit Zone", content)
    elif req.method == "POST":
        data = await req.form()
        try:
            update_zone(zone_id, data)
            return RedirectResponse("/zones", status_code=303)
        except ValueError as e:
            logger.error(f"Error updating zone: {e}")
            content = [
                P(str(e), style="color:red"),
                zone_form(f"/zones/edit/{zone_id}", zone=zone)
            ]
            return page_view(req, "Edit Zone", content)

async def zone_delete_view(req: Request, zone_id: int):
    """Handles deleting an existing zone."""
    zone = get_zone_by_id(zone_id)
    if not zone:
        return page_view(req, "Error", [Div("Zone not found.")])
    if req.method == "POST":
        delete_zone(zone_id)
        return RedirectResponse("/zones", status_code=303)
    else:
        content = [
            H2(f"Are you sure you want to delete {zone.name}?"),
            Form(
                Button("Yes, delete", type="submit", cls="button danger"),
                action=f"/zones/delete/{zone_id}",
                method="post"
            )
        ]
        return page_view(req, "Delete Zone", content)

async def zone_routes_view(req: Request, zone_id: int):
    """View all routes in a specific zone."""
    zone = get_zone_by_id(zone_id)
    if not zone:
        return page_view(req, "Error", [Div("Zone not found.")])

    # Import inside the function to avoid circular import
    from app.components.route.services import get_routes_by_zone_id

    routes = get_routes_by_zone_id(zone_id)
    content = [
        H1(f"Routes in Zone: {zone.name}"),
        Table(
            Thead(
                Tr(
                    Th("ID"), Th("Name"), Th("Description"), Th("Actions")
                )
            ),
            Tbody(
                *[
                    Tr(
                        Td(str(route.id)),
                        Td(route.name),
                        Td(route.description),
                        Td(
                            A("Edit", href=f"/routes/edit/{route.id}", cls="button small"),
                            " ",
                            A("Delete", href=f"/routes/delete/{route.id}", cls="button small danger")
                        )
                    ) for route in routes
                ]
            ),
            cls="table-responsive"
        ),
        A("Add New Route", href=f"/zones/{zone_id}/routes/add", cls="button")
    ]
    return page_view(req, f"Routes in Zone {zone.name}", content)