# components/route/views.py

from fasthtml.common import *
from app.components.route.forms import route_form
from app.components.route.services import (
    get_routes_by_zone_id, get_route_by_id, create_route, update_route, delete_route
)
from app.components.zone.services import get_zone_by_id
from app.components.common.page import page_view
from starlette.responses import RedirectResponse
from starlette.requests import Request
import logging

logger = logging.getLogger(__name__)

async def route_list_view(req: Request, zone_id: int):
    """Generates the route list view for a specific zone."""
    zone = get_zone_by_id(zone_id)
    if not zone:
        return page_view(req, "Error", [Div("Zone not found.")])
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
    return page_view(req, "Route List", content)

async def route_add_view(req: Request, zone_id: int):
    """Handles adding a new route."""
    zone = get_zone_by_id(zone_id)
    if not zone:
        return page_view(req, "Error", [Div("Zone not found.")])

    if req.method == "GET":
        content = [
            route_form(f"/zones/{zone_id}/routes/add", zone_id=zone_id)
        ]
        return page_view(req, "Add Route", content)
    elif req.method == "POST":
        data = await req.form()
        try:
            create_route(data)
            return RedirectResponse(f"/zones/{zone_id}/routes", status_code=303)
        except ValueError as e:
            logger.error(f"Error creating route: {e}")
            content = [
                P(str(e), style="color:red"),
                route_form(f"/zones/{zone_id}/routes/add", zone_id=zone_id)
            ]
            return page_view(req, "Add Route", content)

async def route_edit_view(req: Request, route_id: int):
    """Handles editing an existing route."""
    route = get_route_by_id(route_id)
    if not route:
        return page_view(req, "Error", [Div("Route not found.")])
    if req.method == "GET":
        content = [
            route_form(f"/routes/edit/{route_id}", route=route, zone_id=route.zone_id)
        ]
        return page_view(req, "Edit Route", content)
    elif req.method == "POST":
        data = await req.form()
        try:
            update_route(route_id, data)
            return RedirectResponse(f"/zones/{route.zone_id}/routes", status_code=303)
        except ValueError as e:
            logger.error(f"Error updating route: {e}")
            content = [
                P(str(e), style="color:red"),
                route_form(f"/routes/edit/{route_id}", route=route, zone_id=route.zone_id)
            ]
            return page_view(req, "Edit Route", content)

async def route_delete_view(req: Request, route_id: int):
    """Handles deleting an existing route."""
    route = get_route_by_id(route_id)
    if not route:
        return page_view(req, "Error", [Div("Route not found.")])
    if req.method == "POST":
        delete_route(route_id)
        return RedirectResponse(f"/zones/{route.zone_id}/routes", status_code=303)
    else:
        content = [
            H2(f"Are you sure you want to delete route {route.name}?"),
            Form(
                Button("Yes, delete", type="submit", cls="button danger"),
                action=f"/routes/delete/{route_id}",
                method="post"
            )
        ]
        return page_view(req, "Delete Route", content)