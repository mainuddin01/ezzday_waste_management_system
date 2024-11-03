# components/schedule/forms.py
# forms.py

from fasthtml.common import *
from typing import List

def schedule_form(action_url, method="post", schedule=None, drivers=None, loaders=None):
    """Generates a form for creating or editing a schedule."""
    selected_loader_ids = schedule.loader_ids if schedule else []
    return Form(
        Div(
            Label("Week Number:", For="week_number"),
            Input(
                name="week_number",
                type="number",
                id="week_number",
                value=schedule.week_number if schedule else "",
                placeholder="Enter week number",
                required=True,
                min="1",
                max="52"
            )
        ),
        Div(
            Label("Day of Week:", For="dow"),
            Select(
                *[
                    Option(day, value=day, selected=schedule and schedule.dow == day)
                    for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                ],
                name="dow",
                id="dow",
                required=True
            )
        ),
        Div(
            Label("Driver:", For="driver_id"),
            Select(
                *[
                    Option(f"Driver {driver.id}: {driver.name}", value=driver.id, selected=schedule and schedule.driver_id == driver.id)
                    for driver in drivers
                ],
                name="driver_id",
                id="driver_id",
                required=True
            )
        ),
        Div(
            Label("Loaders:", For="loader_ids"),
            Fieldset(
                *[
                    Div(
                        Input(
                            name="loader_ids",
                            type="checkbox",
                            value=loader.id,
                            id=f"loader_{loader.id}",
                            checked=schedule and loader.id in selected_loader_ids
                        ),
                        Label(f"Loader {loader.id}: {loader.name}", For=f"loader_{loader.id}")
                    )
                    for loader in loaders
                ]
            )
        ),
        Button("Submit", type="submit"),
        action=action_url,
        method=method
    )