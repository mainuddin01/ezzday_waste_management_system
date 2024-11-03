# app/components/common/header.py

from fasthtml.common import *
from app.components.auth.models import User
from app.components.auth.services import decode_token

def header_component(req):
    """Generates the header component with navigation links based on user role."""
    user = get_current_user(req)
    nav_links = []

    if user:
        # Common links for all authenticated users
        nav_links.append(Li(A("Home", href="/")))
        nav_links.append(Li(A("Profile", href="/auth/profile")))

        if user.role == "Admin":
            # Admin-specific navigation links
            nav_links.extend([
                Li(A("Clients", href="/clients")),
                Li(A("Zones", href="/zones")),
                Li(A("Routes", href="/routes")),
                Li(A("Crews", href="/crews")),
                Li(A("Assignments", href="/assignments")),
                Li(A("Fleet", href="/fleet")),
                Li(A("Drivers", href="/drivers")),
                Li(A("Loaders", href="/loaders")),
                Li(A("Schedules", href="/schedules")),
                Li(A("Events", href="/events")),
                Li(A("Reports", href="/reports")),
                Li(A("Issues", href="/issues")),
                Li(A("Users", href="/users")),
            ])
        elif user.role == "Supervisor":
            # Supervisor-specific navigation links
            nav_links.extend([
                Li(A("Assignments", href="/assignments")),
                Li(A("Zones", href="/zones")),
                Li(A("Routes", href="/routes")),
                Li(A("Reports", href="/reports")),
                Li(A("Issues", href="/issues")),
            ])
        elif user.role == "Dispatch":
            # Dispatch-specific navigation links
            nav_links.extend([
                Li(A("Assignments", href="/assignments")),
                Li(A("Attendance", href="/assignments/attendance")),
                Li(A("Status Updates", href="/assignments/status/update/11AM")),
                Li(A("Issues", href="/issues")),
            ])
        # Logout link
        nav_links.append(Li(A("Logout", href="/auth/logout")))
    else:
        # Links for unauthenticated users
        nav_links.append(Li(A("Home", href="/")))
        nav_links.append(Li(A("Login", href="/auth/login")))

    return Header(
        Div(
            Nav(
                A("eZzDay", href="/", cls="logo"),
                Input(type="checkbox", id="nav-toggle"),
                Label(Span(), For="nav-toggle", cls="nav-toggle-label"),
                Ul(*nav_links, cls="nav-menu"),
                cls="nav"
            ),
            cls="container"
        ),
        cls="header"
    )

def get_current_user(req):
    """Helper function to get the current user."""
    access_token = req.session.get('access_token')
    if access_token:
        decoded_token = decode_token(access_token)
        if decoded_token:
            user_id = decoded_token.get('user_id')
            return User.find_by_id(user_id)
    return None