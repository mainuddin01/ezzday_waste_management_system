# components/assignment/routes.py

import logging
from fasthtml.common import *
from starlette.responses import RedirectResponse

# Import views
from app.components.assignment.views import (
    assignment_list_view, assignment_add_view, assignment_edit_view, assignment_delete_view,
    attendance_view, status_update_view
)
from app.components.dashboard.views import admin_dashboard_view, supervisor_dashboard_view, dispatch_dashboard_view

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def requires(roles, redirect=None):
    """Decorator to require specific user roles for access."""
    def decorator(func):
        async def wrapper(request, *args, **kwargs):
            user_role = request.session.get("user_role")
            if user_role in roles:
                return await func(request)
            if redirect:
                return RedirectResponse(redirect)
            return Titled("Unauthorized", Div(H1("Unauthorized"), P("You do not have permission to access this page.")))
        return wrapper
    return decorator

def setup_routes(app):
    # Home/Dashboard routes
    # @app.route("/", methods=["GET"])
    # async def home(req):
    #     user_role = req.session.get("role")
    #     if user_role == "Admin":
    #         return await admin_dashboard_view(req)
    #     elif user_role == "Supervisor":
    #         return await supervisor_dashboard_view(req)
    #     elif user_role == "Dispatch":
    #         return await dispatch_dashboard_view(req)
    #     else:
    #         return RedirectResponse("/auth/login", status_code=303)

    # Assignment management routes
    @app.route("/assignments", methods=["GET"])
    @requires(["Admin", "Supervisor", "Dispatch"], redirect="/auth/login")
    async def list_assignments(req):
        return await assignment_list_view(req)

    @app.route("/assignments/add", methods=["GET", "POST"])
    @requires(["Admin"], redirect="/auth/login")
    async def add_assignment(req):
        return await assignment_add_view(req)

    @app.route("/assignments/edit/{assignment_id}", methods=["GET", "POST"])
    @requires(["Admin"], redirect="/auth/login")
    async def edit_assignment(req, assignment_id):
        return await assignment_edit_view(req, assignment_id)

    @app.route("/assignments/delete/{assignment_id}", methods=["GET", "POST"])
    @requires(["Admin"], redirect="/auth/login")
    async def delete_assignment(req, assignment_id):
        return await assignment_delete_view(req, assignment_id)

    @app.route("/assignments/attendance", methods=["GET", "POST"])
    @requires(["Dispatch"], redirect="/auth/login")
    async def attendance(req):
        return await attendance_view(req)

    @app.route("/assignments/status/update/{time_label}", methods=["GET", "POST"])
    @requires(["Dispatch"], redirect="/auth/login")
    async def status_update(req, time_label):
        return await status_update_view(req, time_label)

    # Error handling
    @app.exception_handler(404)
    async def not_found(req, exc):
        logger.warning(f"404 error: Page not found - {req.url}")
        return Titled("404 Not Found", Div(H1("Page Not Found"), P("Sorry, the page you are looking for does not exist.")))

    @app.exception_handler(500)
    async def server_error(req, exc):
        logger.error(f"500 error: Internal server error - {req.url} - {str(exc)}")
        return Titled("500 Internal Server Error", Div(H1("Server Error"), P("An internal server error occurred. Please try again later.")))

    logger.info("All routes have been successfully registered.")