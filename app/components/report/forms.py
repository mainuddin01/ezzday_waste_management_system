# components/report/forms.py
# forms.py

from fasthtml.common import *
import json

def report_form(action_url, method="post", report_types=None):
    """Generates a form for creating or generating a report."""
    if report_types is None:
        report_types = [
            ("End of Day", "End of Day"),
            ("Issue Report", "Issue Report"),
            ("Schedule Report", "Schedule Report"),
            ("Attendance Report", "Attendance Report"),
            ("Custom Report", "Custom Report")
        ]

    return Form(
        Div(
            Label("Report Type:", For="report_type"),
            Select(
                *[Option(label, value=value) for value, label in report_types],
                name="report_type",
                id="report_type",
                required=True
            )
        ),
        Div(
            Label("Parameters (JSON format):", For="parameters"),
            Textarea(
                name="parameters",
                id="parameters",
                placeholder='{"key": "value"}',
                required=False
            )
        ),
        Button("Generate Report", type="submit"),
        action=action_url,
        method=method
    )