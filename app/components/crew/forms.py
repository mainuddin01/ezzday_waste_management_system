# components/crew/forms.py

from fasthtml.common import *
from app.components.driver.services import get_all_drivers
from app.components.loader.services import get_all_loaders
from app.components.fleet.services import get_all_trucks

def crew_form(action_url, method="post", crew=None):
    """Generates a form for creating or editing a crew."""
    drivers = get_all_drivers()
    trucks = get_all_trucks()
    loaders = get_all_loaders()

    driver_options = [
        Option(f"{driver.name} (ID: {driver.id})", value=driver.id, selected=crew and crew.driver_id == driver.id)
        for driver in drivers
    ]

    truck_options = [
        Option(f"{truck.truck_number} (ID: {truck.id})", value=truck.id, selected=crew and crew.truck_id == truck.id)
        for truck in trucks
    ]

    loader_options = [
        Checkbox(name="loaders", value=loader.id, checked=crew and loader.id in crew.loaders, label=f"{loader.name} (ID: {loader.id})")
        for loader in loaders
    ]

    return Form(
        Div(
            Label("Driver:", For="driver_id"),
            Select(
                *driver_options,
                name="driver_id",
                id="driver_id",
                required=True
            )
        ),
        Div(
            Label("Truck:", For="truck_id"),
            Select(
                *truck_options,
                name="truck_id",
                id="truck_id",
                required=True
            )
        ),
        Fieldset(
            Legend("Loaders"),
            *loader_options
        ),
        Button("Submit", type="submit"),
        action=action_url,
        method=method
    )