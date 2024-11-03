# components/home/views.py

from fasthtml.common import *
from app.components.common.base import base_component

async def home_view(req):
    """Renders the home page."""
    content = [
        Div(
            cls="container",
            children=[
                Section(
                    cls="introduction",
                    children=[
                        H1("Welcome to eZzDay Waste Management System"),
                        P("Efficiently manage clients, routes, zones, and fleet operations in a comprehensive and easy-to-use web application."),
                        P("Use the navigation menu above to get started.")
                    ]
                ),
                Div(
                    cls="dashboard-links",
                    children=[
                        Div(
                            cls="card",
                            children=[
                                H2("Client Management"),
                                P("Manage your clients, add new ones, or update client information."),
                                A("Manage Clients", href="/clients", cls="button")
                            ]
                        ),
                        Div(
                            cls="card",
                            children=[
                                H2("Zone Management"),
                                P("View and manage zones. Assign clients and routes to various zones."),
                                A("Manage Zones", href="/zones", cls="button")
                            ]
                        ),
                        Div(
                            cls="card",
                            children=[
                                H2("Route Management"),
                                P("Configure routes within zones to keep track of collection schedules."),
                                A("Manage Routes", href="/routes", cls="button")
                            ]
                        ),
                        Div(
                            cls="card",
                            children=[
                                H2("Fleet Management"),
                                P("Monitor fleet status and assignments. Manage driver and loader details."),
                                A("Manage Fleet", href="/fleet", cls="button")
                            ]
                        ),
                    ]
                )
            ]
        )
    ]
    return base_component("Home", content, req)