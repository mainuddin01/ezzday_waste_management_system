# components/event/forms.py

from fasthtml.common import *
from app.components.client.services import get_all_clients
from datetime import date

def event_form(action_url, method="post", event=None):
    """Generates a form for creating or editing an event."""
    clients = get_all_clients()
    client_options = [
        Checkbox(
            name="affected_clients",
            value=client.id,
            checked=event and client.id in event.affected_clients,
            label=f"{client.name} (ID: {client.id})"
        ) for client in clients
    ]

    return Form(
        Div(
            Label("Event Name:", For="name"),
            Input(
                name="name",
                type="text",
                id="name",
                value=event.name if event else "",
                placeholder="Enter event name",
                required=True
            )
        ),
        Div(
            Label("Description:", For="description"),
            Textarea(
                name="description",
                id="description",
                required=False
            )(event.description if event else "")
        ),
        Div(
            Label("Event Type:", For="event_type"),
            Select(
                Option("Select Event Type", value="", disabled=True, selected=not event),
                Option("Holiday", value="Holiday", selected=event and event.event_type == "Holiday"),
                Option("Leaf Collection", value="Leaf Collection", selected=event and event.event_type == "Leaf Collection"),
                Option("Special Pickup", value="Special Pickup", selected=event and event.event_type == "Special Pickup"),
                name="event_type",
                id="event_type",
                required=True
            )
        ),
        Div(
            Label("Start Date:", For="start_date"),
            Input(
                name="start_date",
                type="date",
                id="start_date",
                value=event.start_date if event else "",
                required=True,
                min=str(date.today())
            )
        ),
        Div(
            Label("End Date:", For="end_date"),
            Input(
                name="end_date",
                type="date",
                id="end_date",
                value=event.end_date if event else "",
                required=True,
                min=str(date.today())
            )
        ),
        Fieldset(
            Legend("Affected Clients"),
            *client_options
        ),
        Div(
            Label("Additional Information:", For="additional_info"),
            Textarea(
                name="additional_info",
                id="additional_info",
                required=False
            )(event.additional_info if event else "")
        ),
        Button("Submit", type="submit"),
        action=action_url,
        method=method
    )