# components/assignment/forms.py

from fasthtml.common import *

def assignment_form(action_url, method="post", assignment=None, crews=None, routes=None, clients=None, zones=None):
    """Generates a form for creating or editing an assignment."""
    return Form(
        Select(
            Label("Select Crew:", For="crew_id"),
            Select(
                *[Option(f"Crew {crew.id}", value=crew.id, selected=(assignment and assignment.crew_id == crew.id))
                  for crew in crews],
                name="crew_id", id="crew_id", required=True
            )
        ),
        Select(
            Label("Select Route:", For="route_id"),
            Select(
                *[Option(f"Route {route.id}", value=route.id, selected=(assignment and assignment.route_id == route.id))
                  for route in routes],
                name="route_id", id="route_id", required=True
            )
        ),
        Select(
            Label("Select Client:", For="client_id"),
            Select(
                *[Option(f"Client {client.name}", value=client.id, selected=(assignment and assignment.client_id == client.id))
                  for client in clients],
                name="client_id", id="client_id", required=True
            )
        ),
        Select(
            Label("Select Zone:", For="zone_id"),
            Select(
                *[Option(f"Zone {zone.name}", value=zone.id, selected=(assignment and assignment.zone_id == zone.id))
                  for zone in zones],
                name="zone_id", id="zone_id", required=True
            )
        ),
        Div(
            Label("Assignment Date:", For="doc"),
            Input(name="doc", type="date", value=str(assignment.doc) if assignment else "", required=True, id="doc")
        ),
        Div(
            Label("Week Type:", For="week_type"),
            Select(
                Option("Regular", value="Regular", selected=(assignment and assignment.week_type == "Regular")),
                Option("Event", value="Event", selected=(assignment and assignment.week_type == "Event")),
                name="week_type", id="week_type", required=True
            )
        ),
        Button("Submit", type="submit"),
        action=action_url,
        method=method
    )