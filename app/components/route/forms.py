# components/route/forms.py
# forms.py

from fasthtml.common import *
from typing import List

def route_form(action_url, method="post", route=None, zones=None):
    """Generates a form for creating or editing a route."""
    return Form(
        Div(
            Label("Route Name:", For="name"),
            Input(
                name="name",
                type="text",
                id="name",
                value=route.name if route else "",
                placeholder="Enter route name",
                required=True
            )
        ),
        Div(
            Label("Zone:", For="zone_id"),
            Select(
                *[
                    Option(f"Zone {zone.id}: {zone.name}", value=zone.id, selected=route and route.zone_id == zone.id)
                    for zone in zones
                ],
                name="zone_id",
                id="zone_id",
                required=True
            )
        ),
        Div(
            Label("Description:", For="description"),
            Textarea(
                name="description",
                id="description",
                placeholder="Enter route description",
                required=False
            )(route.description if route else "")
        ),
        Button("Submit", type="submit"),
        action=action_url,
        method=method
    )