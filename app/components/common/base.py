# components/common/base.py

from fasthtml.common import *
from app.components.common.header import header_component
from app.components.common.footer import footer_component

def base_component(title, content_components, req):
    """Generates the base HTML structure with header and footer."""
    return Html(
        Lang="en",
        *[
            Head(
                Meta(charset="UTF-8"),
                Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
                Title(f"{title} - eZzDay Waste Management System"),
                Link(rel="stylesheet", href="/static/css/pico.min.css"),
                Link(rel="stylesheet", href="/static/css/components.css"),
                Link(rel="stylesheet", href="/static/css/main.css"),
                Link(rel="icon", href="/static/assets/favicon.ico", type="image/x-icon"),
            ),
            Body(
                header_component(req),
                Main(
                    *content_components,
                    cls="container"
                ),
                footer_component(),  # Ensure this function returns a valid HTML element
                Script(src="/static/js/main.js"),
            )
        ],
        **{"data-theme": "light"},  # Change to "dark" for dark theme
    )