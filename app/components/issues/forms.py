# components/issues/forms.py

from fasthtml.common import *

def issue_form(action_url, method="post", issue=None, crews=None, routes=None):
    """Generates a form for creating or editing an issue."""
    issue_types = [
        ("Nothing Out", "Nothing Out"),
        ("Wrong Collection Week", "Wrong Collection Week"),
        ("Blocked Access", "Blocked Access"),
        ("Safety Hazard", "Safety Hazard"),
        ("Other", "Other")
    ]

    return Form(
        Div(
            Label("Crew:", For="crew_id"),
            Select(
                *[
                    Option(f"Crew {crew.id}", value=crew.id, selected=issue and issue.crew_id == crew.id)
                    for crew in crews
                ],
                name="crew_id",
                id="crew_id",
                required=True
            )
        ),
        Div(
            Label("Route:", For="route_id"),
            Select(
                *[
                    Option(f"Route {route.id}", value=route.id, selected=issue and issue.route_id == route.id)
                    for route in routes
                ],
                name="route_id",
                id="route_id",
                required=True
            )
        ),
        Div(
            Label("Address:", For="address"),
            Input(
                name="address",
                type="text",
                id="address",
                value=issue.address if issue else "",
                placeholder="Enter issue address",
                required=True
            )
        ),
        Div(
            Label("Issue Type:", For="issue_type"),
            Select(
                *[
                    Option(label, value=value, selected=issue and issue.issue_type == value)
                    for value, label in issue_types
                ],
                name="issue_type",
                id="issue_type",
                required=True
            )
        ),
        Div(
            Label("Description:", For="description"),
            Textarea(
                name="description",
                id="description",
                placeholder="Enter issue description",
                required=False
            )(issue.description if issue else "")
        ),
        Button("Submit", type="submit"),
        action=action_url,
        method=method
    )