# components/driver/forms.py

from fasthtml.common import *
from datetime import date

def driver_form(action_url, method="post", driver=None):
    """Generates a form for creating or editing a driver."""
    return Form(
        Div(
            Label("Driver Name:", For="name"),
            Input(
                name="name",
                type="text",
                id="name",
                value=driver.name if driver else "",
                placeholder="Enter driver name",
                required=True
            )
        ),
        Div(
            Label("License Number:", For="license_number"),
            Input(
                name="license_number",
                type="text",
                id="license_number",
                value=driver.license_number if driver else "",
                placeholder="Enter license number",
                required=True
            )
        ),
        Div(
            Label("License Expiry Date:", For="license_expiry"),
            Input(
                name="license_expiry",
                type="date",
                id="license_expiry",
                value=driver.license_expiry if driver else "",
                required=True,
                min=str(date.today())
            )
        ),
        Div(
            Label("Last Medical Check Date:", For="last_medical_check"),
            Input(
                name="last_medical_check",
                type="date",
                id="last_medical_check",
                value=driver.last_medical_check if driver else "",
                required=False,
                max=str(date.today())
            )
        ),
        Button("Submit", type="submit"),
        action=action_url,
        method=method
    )