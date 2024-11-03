# app/components/client/routes.py

import logging
from starlette.responses import RedirectResponse

# Import views
from app.components.client.views import (
    client_list_view, client_add_view, client_edit_view, client_delete_view
)

logger = logging.getLogger(__name__)

def requires(roles, redirect=None):
    """Decorator to require specific user roles for access."""
    def decorator(func):
        async def wrapper(request, *args, **kwargs):
            user_role = request.session.get("user_role")  # Corrected key to match 'user_role' in session
            if user_role in roles:
                return await func(request, *args, **kwargs)
            if redirect:
                return RedirectResponse(redirect)
            return Titled("Unauthorized", Div(H1("Unauthorized"), P("You do not have permission to access this page.")))
        return wrapper
    return decorator

def setup_routes(app):
    # Client management routes
    @app.route("/clients", methods=["GET"])
    @requires(["Admin"], redirect="/auth/login")
    async def list_clients(req):
        return await client_list_view(req)

    @app.route("/clients/add", methods=["GET", "POST"])
    @requires(["Admin"], redirect="/auth/login")
    async def add_client(req):
        return await client_add_view(req)

    @app.route("/clients/edit/{client_id:int}", methods=["GET", "POST"])
    @requires(["Admin"], redirect="/auth/login")
    async def edit_client(req, client_id):
        return await client_edit_view(req, client_id)

    @app.route("/clients/delete/{client_id:int}", methods=["GET", "POST"])
    @requires(["Admin"], redirect="/auth/login")
    async def delete_client(req, client_id):
        return await client_delete_view(req, client_id)

    logger.info("Client routes have been successfully registered.")

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