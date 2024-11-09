# app/components/dashboard/views.py

import logging
from fasthtml.common import *
from datetime import date
from app.components.common.page import page_view
from app.components.auth.utils import get_current_user
from starlette.responses import RedirectResponse
from starlette.requests import Request

logger = logging.getLogger(__name__)

# Admin Dashboard View
async def user_management_view(req: Request):
    """
    Generates the user management view for admins to monitor and manage all users.
    Only accessible by users with 'Admin' role.
    """
    user = get_current_user(req)
    if user is None or user.role != "Admin":
        logger.warning(f"Unauthorized access attempt to admin dashboard.")
        return RedirectResponse("/auth/login", status_code=303)

    try:
        # Function-level imports to prevent circular dependencies
        from app.components.auth.models import User

        users = User.find_all()
    except Exception as e:
        logger.error(f"Error fetching data for user management view: {e}")
        return page_view(req, "Error", [Div("An error occurred while loading the user items.")])

    content = [
        H2("User Management"),
        Ul(*[
            Li(
                Div(f"User ID: {user.id}"),
                Div(f"Username: {user.username}"),
                Div(f"Role: {user.role}"),
                Div(A("Edit User", href=f"/users/edit/{user.id}")),
                Div(A("Delete User", href=f"/users/delete/{user.id}", cls="button small danger"))
            ) for user in users
        ]) if users else P("No users available."),
    ]
    return page_view(req, "Users", content)

# Admin Dashboard View
async def admin_dashboard_view(req: Request):
    """
    Generates the dashboard view for admins to monitor and manage all aspects of the system.
    Only accessible by users with 'Admin' role.
    """
    user = get_current_user(req)
    if user is None or user.role != "Admin":
        logger.warning(f"Unauthorized access attempt to admin dashboard.")
        return RedirectResponse("/auth/login", status_code=303)

    try:
        # Function-level imports to prevent circular dependencies
        from app.components.client.models import Client
        from app.components.fleet.models import Truck
        from app.components.auth.models import User

        clients = Client.find_all()
        trucks = Truck.find_all()
        users = User.find_all()
    except Exception as e:
        logger.error(f"Error fetching data for admin dashboard: {e}")
        return page_view(req, "Error", [Div("An error occurred while loading the dashboard.")])

    content = [
        H1("Admin Dashboard - System Overview"),
        H2("Clients Overview"),
        Ul(*[
            Li(
                Div(A(f"Client Name: {client.name}", href=f"/clients/view/{client.id}")),
                Div(f"Client Type: {client.client_type}")
            ) for client in clients
        ]) if clients else P("No clients available."),
        H2("Fleet Overview"),
        Ul(*[
            Li(
                Div(A(f"Truck Number: {truck.truck_number}", href=f"/fleet/view/{truck.id}")),
                Div(f"Type: {truck.truck_type}"),
                Div(f"Status: {truck.status}")
            ) for truck in trucks
        ]) if trucks else P("No fleet vehicles available.")
    ]
    return page_view(req, "Admin Dashboard", content)

# Supervisor Dashboard View
async def supervisor_dashboard_view(req: Request):
    """
    Generates the dashboard view for supervisors to monitor schedules and assignments.
    Only accessible by users with 'Supervisor' role.
    """
    user = get_current_user(req)
    if user is None or user.role != "Supervisor":
        logger.warning(f"Unauthorized access attempt to supervisor dashboard.")
        return RedirectResponse("/auth/login", status_code=303)

    try:
        from app.components.schedule.models import Schedule
        from app.components.assignment.models import Assignment

        schedules = Schedule.find_all()
        assignments = Assignment.find_all_for_date(date.today())
    except Exception as e:
        logger.error(f"Error fetching data for supervisor dashboard: {e}")
        return page_view(req, "Error", [Div("An error occurred while loading the dashboard.")])

    content = [
        H1("Supervisor Dashboard - Schedule & Assignment Monitoring"),
        H2("Schedules Overview"),
        Ul(*[
            Li(
                Div(f"Schedule ID: {schedule.id}"),
                Div(f"Week Number: {schedule.week_number}"),
                Div(f"Day of Week: {schedule.dow}"),
                Div(f"Driver ID: {schedule.driver_id}"),
                Div(f"Loader IDs: {', '.join(map(str, schedule.loader_ids))}"),
                Div(f"Notification Sent: {'Yes' if schedule.notification_sent else 'No'}"),
                Div(f"Attendance Marked: {'Yes' if schedule.attendance_marked else 'No'}"),
                Div(A("View Details", href=f"/schedules/view/{schedule.id}"))
            ) for schedule in schedules
        ]) if schedules else P("No schedules available."),
        H2("Today's Assignments Overview"),
        Ul(*[
            Li(
                Div(f"Assignment ID: {assignment.id}"),
                Div(A(f"Crew ID: {assignment.crew_id}", href=f"/crews/view/{assignment.crew_id}")),
                Div(f"Route ID: {assignment.route_id}"),
                Div(A(f"Client ID: {assignment.client_id}", href=f"/clients/view/{assignment.client_id}")),
                Div(f"Zone ID: {assignment.zone_id}"),
                Div(f"Completion Time: {assignment.completion_time} hours" if assignment.completion_time else "Not yet completed"),
                Div(A("View Assignment", href=f"/assignments/view/{assignment.id}"))
            ) for assignment in assignments
        ]) if assignments else P("No assignments for today."),
    ]
    return page_view(req, "Supervisor Dashboard", content)

# Dispatch Dashboard View
async def dispatch_dashboard_view(req: Request):
    """
    Generates the dashboard view for dispatchers to monitor all assignments.
    Only accessible by users with 'Dispatch' role.
    """
    user = get_current_user(req)
    if user is None or user.role != "Dispatch":
        logger.warning(f"Unauthorized access attempt to dispatch dashboard.")
        return RedirectResponse("/auth/login", status_code=303)

    try:
        from app.components.assignment.models import Assignment

        assignments = Assignment.find_all_for_date(date.today())
    except Exception as e:
        logger.error(f"Error fetching data for dispatch dashboard: {e}")
        return page_view(req, "Error", [Div("An error occurred while loading the dashboard.")])

    content = [
        H1("Dispatcher Dashboard - Daily Assignment Overview"),
        Ul(*[
            Li(
                Div(f"Assignment ID: {assignment.id}"),
                Div(A(f"Crew ID: {assignment.crew_id}", href=f"/crews/view/{assignment.crew_id}")),
                Div(f"Route ID: {assignment.route_id}"),
                Div(A(f"Client ID: {assignment.client_id}", href=f"/clients/view/{assignment.client_id}")),
                Div(f"Zone ID: {assignment.zone_id}"),
                Div(f"Week Number: {assignment.week_number}"),
                Div(f"Day of Week: {assignment.dow}"),
                Div(f"Attendance Confirmed: {'Yes' if assignment.attendance_confirmed else 'No'}"),
                Div(f"PPE Compliance: {'Yes' if assignment.ppe_compliance else 'No'}"),
                Div(f"11 AM Status: {assignment.status_updates.get('11AM', 'Pending')}"),
                Div(f"1 PM Status: {assignment.status_updates.get('1PM', 'Pending')}"),
                Div(f"3 PM Status: {assignment.status_updates.get('3PM', 'Pending')}"),
                Div(f"EOD Status: {assignment.status_updates.get('EOD', 'Pending')}"),
                Div(f"Completion Time: {assignment.completion_time} hours" if assignment.completion_time else "Not yet completed"),
                Div(A("Update Status", href=f"/assignments/status/update/{assignment.id}")),
                Div(A("Mark Attendance", href=f"/assignments/attendance/{assignment.id}"))
            ) for assignment in assignments
        ]) if assignments else P("No assignments for today."),
    ]
    return page_view(req, "Dispatcher Dashboard", content)