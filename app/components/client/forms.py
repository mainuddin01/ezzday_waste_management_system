# components/client/forms.py

from fasthtml.common import *
from app.components.zone.services import get_all_zones

def client_form(action_url, method="post", client=None):
    """Generates a form for creating or editing a client."""
    zones = get_all_zones()
    zones_options = [
        Option(zone.name, value=zone.id, selected=(client and zone.id in client.zones_serviced))
        for zone in zones
    ]

    return Form(
        Div(
            Label("Client Name:", For="name"),
            Input(name="name", type="text", id="name", value=client.name if client else "", required=True)
        ),
        Div(
            Label("Client Type:", For="client_type"),
            Select(
                Option("Select Client Type", value="", disabled=True, selected=not client),
                Option("Contractors", value="Contractors", selected=client and client.client_type == "Contractors"),
                Option("Subcontractors", value="Subcontractors", selected=client and client.client_type == "Subcontractors"),
                Option("Private Residents", value="Private Residents", selected=client and client.client_type == "Private Residents"),
                Option("Rear Loader Bin Clients", value="Rear Loader Bin Clients", selected=client and client.client_type == "Rear Loader Bin Clients"),
                Option("Roll-off Bin Clients", value="Roll-off Bin Clients", selected=client and client.client_type == "Roll-off Bin Clients"),
                name="client_type", id="client_type", required=True
            )
        ),
        Div(
            Label("Description:", For="description"),
            Textarea(name="description", id="description", required=False)(client.description if client else "")
        ),
        Div(
            Label("Contact Name:", For="contact_name"),
            Input(name="contact_name", type="text", id="contact_name", value=client.contact_name if client else "", required=True)
        ),
        Div(
            Label("Contact Phone:", For="contact_phone"),
            Input(name="contact_phone", type="tel", id="contact_phone", value=client.contact_phone if client else "", required=True)
        ),
        Div(
            Label("Contact Email:", For="contact_email"),
            Input(name="contact_email", type="email", id="contact_email", value=client.contact_email if client else "", required=True)
        ),
        Div(
            Label("Zones Serviced:", For="zones_serviced"),
            Select(
                *zones_options,
                name="zones_serviced",
                id="zones_serviced",
                multiple=True,
                required=True
            )
        ),
        Button("Submit", type="submit"),
        action=action_url,
        method=method
    )