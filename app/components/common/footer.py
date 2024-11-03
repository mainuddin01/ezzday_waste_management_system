# app/components/common/footer.py
from datetime import datetime
from fasthtml.common import *

def footer_component():
    """Generates the footer component."""
    current_year = datetime.now().year
    return Footer(
        Div(
            P(f"© {current_year} eZzDay Waste Management System. All rights reserved."),
            P(
                A("Contact Us", href="/contact"), " | ",
                A("Terms of Service", href="/terms"), " | ",
                A("Privacy Policy", href="/privacy")
            ),
            cls="container"
        ),
        cls="footer"
    )