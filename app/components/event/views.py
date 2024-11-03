# components/event/views.py

from fasthtml.common import *
from app.components.event.forms import event_form
from app.components.event.services import (
    get_all_events, get_event_by_id, create_event, update_event, delete_event
)
from app.components.common.page import page_view
from starlette.responses import RedirectResponse
from starlette.requests import Request
import logging

logger = logging.getLogger(__name__)

async def event_list_view(req: Request):
    """Generates the event list view."""
    events = get_all_events()
    content = [
        H1("Events"),
        Table(
            Thead(
                Tr(
                    Th("ID"), Th("Name"), Th("Date"), Th("Actions")
                )
            ),
            Tbody(
                *[
                    Tr(
                        Td(str(event.id)),
                        Td(event.name),
                        Td(event.date.isoformat()),
                        Td(
                            A("Edit", href=f"/events/edit/{event.id}", cls="button small"),
                            " ",
                            A("Delete", href=f"/events/delete/{event.id}", cls="button small danger")
                        )
                    ) for event in events
                ]
            ),
            cls="table-responsive"
        ),
        A("Add New Event", href="/events/add", cls="button")
    ]
    return page_view(req, "Event List", content)

async def event_add_view(req: Request):
    """Handles adding a new event."""
    if req.method == "GET":
        content = [
            event_form("/events/add")
        ]
        return page_view(req, "Add Event", content)
    elif req.method == "POST":
        data = await req.form()
        try:
            create_event(data)
            return RedirectResponse("/events", status_code=303)
        except ValueError as e:
            logger.error(f"Error creating event: {e}")
            content = [
                P(str(e), style="color:red"),
                event_form("/events/add")
            ]
            return page_view(req, "Add Event", content)

async def event_edit_view(req: Request, event_id: int):
    """Handles editing an existing event."""
    event = get_event_by_id(event_id)
    if not event:
        return page_view(req, "Error", [Div("Event not found.")])

    if req.method == "GET":
        content = [
            event_form(f"/events/edit/{event_id}", event=event)
        ]
        return page_view(req, "Edit Event", content)
    elif req.method == "POST":
        data = await req.form()
        try:
            update_event(event_id, data)
            return RedirectResponse("/events", status_code=303)
        except ValueError as e:
            logger.error(f"Error updating event: {e}")
            content = [
                P(str(e), style="color:red"),
                event_form(f"/events/edit/{event_id}", event=event)
            ]
            return page_view(req, "Edit Event", content)

async def event_delete_view(req: Request, event_id: int):
    """Handles deleting an existing event."""
    event = get_event_by_id(event_id)
    if not event:
        return page_view(req, "Error", [Div("Event not found.")])

    if req.method == "POST":
        delete_event(event_id)
        return RedirectResponse("/events", status_code=303)
    else:
        content = [
            H2(f"Are you sure you want to delete event '{event.name}'?"),
            Form(
                Button("Yes, delete", type="submit", cls="button danger"),
                action=f"/events/delete/{event_id}",
                method="post"
            )
        ]
        return page_view(req, "Delete Event", content)