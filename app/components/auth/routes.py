# app/components/auth/routes.py

import logging
from starlette.responses import RedirectResponse
from .views import (
    register_view, login_view, logout_view, profile_view, refresh_token_view
)
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)


def setup_routes(app):
    """
    Registers all authentication-related routes with the FastHTML application.
    """

    # Home/Dashboard route
    @app.route("/", methods=["GET"])
    async def home(req: Request):
        user_role = req.session.get("user_role")  # Use consistent session key
        if user_role == "Admin":
            from app.components.dashboard.views import admin_dashboard_view
            return await admin_dashboard_view(req)
        elif user_role == "Supervisor":
            from app.components.dashboard.views import supervisor_dashboard_view
            return await supervisor_dashboard_view(req)
        elif user_role == "Dispatch":
            from app.components.dashboard.views import dispatch_dashboard_view
            return await dispatch_dashboard_view(req)
        else:
            return RedirectResponse("/auth/login", status_code=303)
        
    @app.route("/users", methods=["GET"])
    async def users(req: Request):
        user_role = req.session.get("user_role")  # Use consistent session key
        if user_role == "Admin":
            from app.components.dashboard.views import user_management_view
            return await user_management_view(req)

    # Authentication routes
    @app.route("/auth/register", methods=["GET", "POST"])
    async def register(req: Request):
        return await register_view(req)

    @app.route("/auth/login", methods=["GET", "POST"])
    async def login(req: Request):
        return await login_view(req)

    @app.route("/auth/logout", methods=["GET"])
    async def logout(req: Request):
        return await logout_view(req)

    @app.route("/auth/refresh", methods=["POST"])
    async def refresh_token(req: Request):
        return await refresh_token_view(req)

    # Profile route
    @app.route("/auth/profile", methods=["GET"])
    async def profile(req: Request):
        return await profile_view(req)

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

    logger.info("Authentication routes have been successfully registered.")