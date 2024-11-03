# components/loader/forms.py
# forms.py

from fasthtml.common import *

def loader_form(action_url, method="post", loader=None):
    """Generates a form for creating or editing a loader."""
    return Form(
        Div(
            Label("Loader Name:", For="name"),
            Input(
                name="name",
                type="text",
                id="name",
                value=loader.name if loader else "",
                placeholder="Enter loader name",
                required=True
            )
        ),
        Div(
            Label("Pickup Spot:", For="pickup_spot"),
            Input(
                name="pickup_spot",
                type="text",
                id="pickup_spot",
                value=loader.pickup_spot if loader else "",
                placeholder="Enter pickup spot",
                required=True
            )
        ),
        Button("Submit", type="submit"),
        action=action_url,
        method=method
    )