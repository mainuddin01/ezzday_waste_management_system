# components/fleet/routes.py

import logging
from starlette.responses import RedirectResponse

# Import views
from app.components.fleet.views import (
    fleet_list_view, fleet_add_view, fleet_edit_view, fleet_delete_view, fleet_view
)
from app.components.dashboard.views import (
    admin_dashboard_view, supervisor_dashboard_view, dispatch_dashboard_view
)

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

    # Fleet management routes
    @app.route("/fleet", methods=["GET"])
    @requires(["Admin", "Supervisor"], redirect="/auth/login")
    async def list_fleet(req):
        return await fleet_list_view(req)

    @app.route("/fleet/add", methods=["GET", "POST"])
    @requires("Admin", redirect="/auth/login")
    async def add_fleet(req):
        return await fleet_add_view(req)

    @app.route("/fleet/edit/{truck_id:int}", methods=["GET", "POST"])
    @requires("Admin", redirect="/auth/login")
    async def edit_fleet(req, truck_id):
        return await fleet_edit_view(req, truck_id)

    @app.route("/fleet/delete/{truck_id:int}", methods=["GET", "POST"])
    @requires("Admin", redirect="/auth/login")
    async def delete_fleet(req, truck_id):
        return await fleet_delete_view(req, truck_id)

    @app.route("/fleet/view/{truck_id:int}", methods=["GET"])
    @requires(["Admin", "Supervisor"], redirect="/auth/login")
    async def view_fleet(req, truck_id):
        return await fleet_view(req, truck_id)

    # Error handling
    @app.exception_handler(404)
    async def not_found(req, exc):
        logger.warning(f"404 error: Page not found - {req.url}")
        return Titled("404 Not Found",
            H1("Page Not Found"),
            P("Sorry, the page you are looking for does not exist.")
        )

    @app.exception_handler(500)
    async def server_error(req, exc):
        logger.error(f"500 error: Internal server error - {req.url} - {str(exc)}")
        return Titled("500 Internal Server Error",
            H1("Server Error"),
            P("An internal server error occurred. Please try again later.")
        )

    logger.info("All routes have been successfully registered.")