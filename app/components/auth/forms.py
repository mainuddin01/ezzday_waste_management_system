# app/components/auth/forms.py

from fasthtml.common import *

def registration_form(action_url, zone=None):
    """Generates the registration form."""
    return Form(
        action=action_url,
        method="post",
        cls="form",
        children=[
            Label("Username:", For="username"),
            Input(type="text", name="username", id="username", required=True, placeholder="Enter username"),

            Label("Password:", For="password"),
            Input(type="password", name="password", id="password", required=True, placeholder="Enter password"),

            Label("Confirm Password:", For="confirm_password"),
            Input(type="password", name="confirm_password", id="confirm_password", required=True, placeholder="Confirm password"),

            Label("Role:", For="role"),
            Select(
                name="role",
                id="role",
                required=True,
                children=[
                    Option("Select a Role", value="", disabled=True, selected=True),
                    Option("Admin", value="Admin"),
                    Option("Supervisor", value="Supervisor"),
                    Option("Dispatch", value="Dispatch"),
                ]
            ),

            Button("Register User", type="submit", cls="button")
        ]
    )


def login_form(action_url):
    """Generates the login form."""
    return Form(
        Label("Username:", For="username"),
        Input(type="text", name="username", id="username", required=True, placeholder="Enter username"),

        Label("Password:", For="password"),
        Input(type="password", name="password", id="password", required=True, placeholder="Enter password"),

        Button("Login", type="submit", cls="button"),
        action=action_url,
        method="post",
        cls="form",
    )