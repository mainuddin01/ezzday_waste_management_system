# app/components/auth/views.py

from fasthtml.common import *
from app.components.auth.forms import registration_form, login_form
from app.components.auth.models import User
from app.components.auth.services import (
    register_user, authenticate_user, login_user, refresh_access_token
)
from app.components.common.page import page_view
from starlette.responses import RedirectResponse
from starlette.requests import Request
import logging

# Import the utility function instead of defining it here
from app.components.auth.utils import get_current_user

logger = logging.getLogger(__name__)


async def home_view(req: Request):
    """Handles the home page view."""
    user = get_current_user(req)
    if user:
        content = [
            H1(f"Welcome back, {user.username}!"),
            P(f"Role: {user.role}"),
            A("Profile", href="/profile", cls="link"),  # Changed to /profile
            A("Logout", href="/auth/logout", cls="link")
        ]
    else:
        content = [
            H1("Welcome to eZzDay Waste Management System"),
            A("Login", href="/auth/login", cls="link")
        ]
    return page_view(req, "Home", content)


async def register_view(req: Request):
    """Handles user registration. Accessible only by admin users."""
    user = get_current_user(req)
    if user is None or user.role != 'Admin':
        logger.warning(f"Unauthorized registration attempt by user: {user.username if user else 'Unknown'}")
        return RedirectResponse("/auth/login", status_code=303)

    if req.method == "GET":
        content = [registration_form("/auth/register")]
        return page_view(req, "Register", content)

    elif req.method == "POST":
        data = await req.form()
        try:
            register_user(data)
            logger.info(f"New user registered: {data.get('username')}")
            return RedirectResponse("/users", status_code=303)
        except ValueError as e:
            logger.error(f"Registration error: {str(e)}")
            content = [
                Div(P(str(e), cls="alert error")),
                registration_form("/auth/register")
            ]
            return page_view(req, "Register Error", content)
        except Exception as e:
            logger.exception(f"Unexpected error during registration: {e}")
            content = [
                Div(P("An unexpected error occurred during registration.", cls="alert error")),
                registration_form("/auth/register")
            ]
            return page_view(req, "Register Error", content)


async def login_view(req: Request):
    """Handles user login."""
    if req.method == "GET":
        content = [login_form("/auth/login")]
        return page_view(req, "Login", content)

    elif req.method == "POST":
        data = await req.form()
        try:
            tokens = login_user(data['username'], data['password'])
            req.session['access_token'] = tokens['access_token']
            req.session['refresh_token'] = tokens['refresh_token']
            req.session['user_role'] = tokens['user_role']
            req.session['username'] = tokens['username']
            logger.info(f"User '{data['username']}' logged in successfully.")
            return RedirectResponse("/", status_code=303)
        except ValueError as e:
            logger.error(f"Login failed for '{data.get('username')}': {str(e)}")
            content = [
                Div(P("Invalid username or password.", cls="alert error")),
                login_form("/auth/login")
            ]
            return page_view(req, "Login Failed", content)
        except Exception as e:
            logger.exception(f"Unexpected error during login for '{data.get('username')}': {e}")
            content = [
                Div(P("An unexpected error occurred during login.", cls="alert error")),
                login_form("/auth/login")
            ]
            return page_view(req, "Login Failed", content)


async def logout_view(req: Request):
    """Handles user logout by clearing session tokens."""
    username = req.session.get('username', 'Unknown')
    req.session.clear()
    logger.info(f"User '{username}' logged out.")
    return RedirectResponse("/auth/login", status_code=303)


async def refresh_token_view(req: Request):
    """Handles the refresh token request to provide a new access token."""
    refresh_token = req.session.get('refresh_token')
    if not refresh_token:
        logger.warning("Refresh token missing in session.")
        return RedirectResponse("/auth/login", status_code=303)

    try:
        new_access_token = refresh_access_token(refresh_token)
        req.session['access_token'] = new_access_token
        logger.info("Access token refreshed successfully.")
        return RedirectResponse("/", status_code=303)
    except ValueError as e:
        logger.error(f"Token refresh error: {str(e)}")
        content = [
            Div(P("Session expired. Please log in again.", cls="alert error")),
            A("Login Again", href="/auth/login", cls="button")
        ]
        return page_view(req, "Session Expired", content)


async def profile_view(req: Request):
    """Displays user profile information. Protected by authentication."""
    user = get_current_user(req)
    if user is None:
        logger.warning("Unauthorized access to profile page.")
        return RedirectResponse("/auth/login", status_code=303)

    content = [
        H1(f"Welcome, {user.username}!"),
        P(f"Role: {user.role}"),
        A("Logout", href="/auth/logout", cls="button")
    ]
    return page_view(req, "Profile", content)