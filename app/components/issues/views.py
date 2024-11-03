# components/issues/views.py

from fasthtml.common import *
from app.components.issues.forms import issue_form
from app.components.issues.services import (
    get_all_issues, get_issue_by_id, create_issue, update_issue, delete_issue
)
from app.components.crew.services import get_all_crews
from app.components.route.services import get_all_routes
from app.components.common.page import page_view
from starlette.responses import RedirectResponse
from starlette.requests import Request
import logging

logger = logging.getLogger(__name__)

async def issue_list_view(req: Request):
    """Generates the issue list view."""
    issues = get_all_issues()
    content = [
        H1("Issues"),
        Table(
            Thead(
                Tr(
                    Th("ID"), Th("Type"), Th("Description"), Th("Reported By"), Th("Actions")
                )
            ),
            Tbody(
                *[
                    Tr(
                        Td(str(issue.id)),
                        Td(issue.issue_type),
                        Td(issue.description),
                        Td(str(issue.reported_by)),
                        Td(
                            A("Edit", href=f"/issues/edit/{issue.id}", cls="button small"),
                            " ",
                            A("Delete", href=f"/issues/delete/{issue.id}", cls="button small danger")
                        )
                    ) for issue in issues
                ]
            ),
            cls="table-responsive"
        ),
        A("Report New Issue", href="/issues/add", cls="button")
    ]
    return page_view(req, "Issue List", content)

async def issue_add_view(req: Request):
    """Handles adding a new issue."""
    crews = get_all_crews()
    routes = get_all_routes()

    if req.method == "GET":
        content = [
            issue_form("/issues/add", crews=crews, routes=routes)
        ]
        return page_view(req, "Report Issue", content)
    elif req.method == "POST":
        data = await req.form()
        try:
            create_issue(data)
            return RedirectResponse("/issues", status_code=303)
        except ValueError as e:
            logger.error(f"Error creating issue: {e}")
            content = [
                P(str(e), style="color:red"),
                issue_form("/issues/add", crews=crews, routes=routes)
            ]
            return page_view(req, "Report Issue", content)

async def issue_edit_view(req: Request, issue_id: int):
    """Handles editing an existing issue."""
    issue = get_issue_by_id(issue_id)
    if not issue:
        return page_view(req, "Error", [Div("Issue not found.")])
    crews = get_all_crews()
    routes = get_all_routes()

    if req.method == "GET":
        content = [
            issue_form(f"/issues/edit/{issue_id}", issue=issue, crews=crews, routes=routes)
        ]
        return page_view(req, "Edit Issue", content)
    elif req.method == "POST":
        data = await req.form()
        try:
            update_issue(issue_id, data)
            return RedirectResponse("/issues", status_code=303)
        except ValueError as e:
            logger.error(f"Error updating issue: {e}")
            content = [
                P(str(e), style="color:red"),
                issue_form(f"/issues/edit/{issue_id}", issue=issue, crews=crews, routes=routes)
            ]
            return page_view(req, "Edit Issue", content)

async def issue_delete_view(req: Request, issue_id: int):
    """Handles deleting an existing issue."""
    issue = get_issue_by_id(issue_id)
    if not issue:
        return page_view(req, "Error", [Div("Issue not found.")])
    if req.method == "POST":
        delete_issue(issue_id)
        return RedirectResponse("/issues", status_code=303)
    else:
        content = [
            H2(f"Are you sure you want to delete issue {issue.id}?"),
            Form(
                Button("Yes, delete", type="submit", cls="button danger"),
                action=f"/issues/delete/{issue_id}",
                method="post"
            )
        ]
        return page_view(req, "Delete Issue", content)

async def tracking_board_view(req: Request):
    """Generates the view for tracking repeat offenders."""
    repeat_addresses = get_repeat_offenders()
    content = [
        H1("Repeat Offender Addresses"),
        Ul(*[Li(f"Address: {address}") for address in repeat_addresses])
    ]
    return page_view(req, "Tracking Board - Repeat Offenders", content)