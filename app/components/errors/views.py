# components/errors/views.py

from fasthtml.common import *
from app.components.common.base import base_component

async def not_found_view(req, exc):
    """Handles 404 Not Found errors."""
    content = [
        Div(
            cls="container",
            children=[
                Div(
                    cls="error-page",
                    children=[
                        H1("404 - Page Not Found"),
                        P("Sorry, the page you are looking for does not exist."),
                        P([
                            "You can go back to the ",
                            A("home page", href="/"),
                            " or use the navigation menu above."
                        ])
                    ]
                )
            ]
        )
    ]
    return base_component("404 Not Found", content, req)

async def internal_error_view(req, exc):
    """Handles 500 Internal Server Errors."""
    content = [
        Div(
            cls="container",
            children=[
                Div(
                    cls="error-page",
                    children=[
                        H1("500 - Internal Server Error"),
                        P("Oops! Something went wrong on our end."),
                        P("Please try refreshing the page, or come back later."),
                        P([
                            "If the problem persists, feel free to ",
                            A("contact us", href="/contact"),
                            "."
                        ])
                    ]
                )
            ]
        )
    ]
    return base_component("500 Internal Server Error", content, req)