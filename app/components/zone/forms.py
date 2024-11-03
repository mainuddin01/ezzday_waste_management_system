# components/zone/forms.py
# forms.py

from fasthtml.common import *
from typing import List

def zone_form(action_url, method="post", zone=None, clients=None):
    """Generates a form for creating or editing a zone."""
    return Form(
        Div(
            Label("Zone Name:", For="name"),
            Input(
                name="name",
                type="text",
                id="name",
                value=zone.name if zone else "",
                placeholder="Enter zone name",
                required=True
            )
        ),
        Div(
            Label("Client:", For="client_id"),
            Select(
                *[
                    Option(f"Client {client.id}: {client.name}", value=client.id, selected=zone and zone.client_id == client.id)
                    for client in clients
                ],
                name="client_id",
                id="client_id",
                required=True
            )
        ),
        Div(
            Label("Description:", For="description"),
            Textarea(
                name="description",
                id="description",
                placeholder="Enter zone description",
                required=False
            )(zone.description if zone else "")
        ),
        Button("Submit", type="submit"),
        action=action_url,
        method=method
    )