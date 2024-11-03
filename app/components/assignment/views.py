# components/assignment/views.py

from fasthtml.common import *
from .forms import assignment_form
from .services import (
    get_assignments_for_date, get_assignment_by_id, create_assignment, update_assignment, delete_assignment
)
from app.components.common.base import base_component
from app.components.common.page import page_view
from app.components.crew.services import get_all_crews
from app.components.route.services import get_all_routes
from app.components.client.services import get_all_clients
from app.components.zone.services import get_all_zones
from datetime import date
from starlette.responses import RedirectResponse
from starlette.requests import Request

async def assignment_list_view(req: Request):
    """Renders the assignment list view for a specific date."""
    assignment_date = req.query_params.get("date", str(date.today()))
    assignments = get_assignments_for_date(assignment_date)

    content = [
        H1(f"Assignments for {assignment_date}"),
        Table(
            Thead(
                Tr(
                    Th("ID"), Th("Crew"), Th("Route"), Th("Client"), Th("Zone"), Th("Date"), Th("Actions")
                )
            ),
            Tbody(
                *[
                    Tr(
                        Td(str(assignment.id)),
                        Td(str(assignment.crew_id)),
                        Td(str(assignment.route_id)),
                        Td(str(assignment.client_id)),
                        Td(str(assignment.zone_id)),
                        Td(str(assignment.doc)),
                        Td(
                            A("Edit", href=f"/assignments/edit/{assignment.id}", cls="button small"),
                            " ",
                            A("Delete", href=f"/assignments/delete/{assignment.id}", cls="button small danger")
                        )
                    ) for assignment in assignments
                ]
            ),
            cls="table-responsive"
        ),
        A("Add New Assignment", href=f"/assignments/add?date={assignment_date}", cls="button")
    ]
    return page_view(req, "Assignment List", content)

async def assignment_add_view(req: Request):
    """Handles adding a new assignment."""
    if req.method == "GET":
        crews = get_all_crews()
        routes = get_all_routes()
        clients = get_all_clients()
        zones = get_all_zones()
        content = [
            assignment_form("/assignments/add", crews=crews, routes=routes, clients=clients, zones=zones)
        ]
        return page_view(req, "Add Assignment", content)
    elif req.method == "POST":
        data = await req.form()
        create_assignment(data)
        return RedirectResponse("/assignments", status_code=303)

async def assignment_edit_view(req: Request, assignment_id: int):
    """Handles editing an existing assignment."""
    assignment = get_assignment_by_id(assignment_id)
    if not assignment:
        return page_view(req, "Error", [Div("Assignment not found.")])

    if req.method == "GET":
        crews = get_all_crews()
        routes = get_all_routes()
        clients = get_all_clients()
        zones = get_all_zones()
        content = [
            assignment_form(f"/assignments/edit/{assignment_id}", assignment=assignment,
                            crews=crews, routes=routes, clients=clients, zones=zones)
        ]
        return page_view(req, "Edit Assignment", content)
    elif req.method == "POST":
        data = await req.form()
        update_assignment(assignment_id, data)
        return RedirectResponse("/assignments", status_code=303)

async def assignment_delete_view(req: Request, assignment_id: int):
    """Handles deleting an existing assignment."""
    assignment = get_assignment_by_id(assignment_id)
    if not assignment:
        return page_view(req, "Error", [Div("Assignment not found.")])

    if req.method == "POST":
        delete_assignment(assignment_id)
        return RedirectResponse("/assignments", status_code=303)
    else:
        content = [
            H2(f"Are you sure you want to delete assignment {assignment.id}?"),
            Form(
                Button("Yes, delete", type="submit", cls="button danger"),
                action=f"/assignments/delete/{assignment_id}",
                method="post"
            )
        ]
        return page_view(req, "Delete Assignment", content)

async def status_update_view(req: Request, time_label: str):
    """Handles status updates for assignments at key times."""
    assignments = get_assignments_for_date(str(date.today()))
    if req.method == "GET":
        content = [
            H1(f"Status Update at {time_label}"),
            Div(
                cls="grid",
                children=[
                    Div(
                        cls="card",
                        children=[
                            H2(f"Crew {assignment.crew_id}"),
                            P(f"Assignment ID: {assignment.id}"),
                            Form(
                                Textarea(name="status", rows="4", placeholder="Enter status details..."),
                                Input(type="hidden", name="assignment_id", value=assignment.id),
                                Button("Submit", type="submit", cls="button"),
                                action=f"/assignments/status/update/{time_label}",
                                method="post",
                                cls="form"
                            )
                        ]
                    ) for assignment in assignments
                ]
            )
        ]
        return page_view(req, f"Status Update - {time_label}", content)
    elif req.method == "POST":
        data = await req.form()
        assignment_id = int(data.get("assignment_id"))
        status = data.get("status")
        assignment = get_assignment_by_id(assignment_id)
        if assignment:
            assignment.update_status(time_label, status)
        return RedirectResponse(f"/assignments/status/update/{time_label}", status_code=303)

async def attendance_view(req: Request):
    """Handles attendance and PPE compliance confirmation."""
    assignments = get_assignments_for_date(str(date.today()))
    if req.method == "GET":
        content = [
            H1("Attendance & PPE Compliance Check"),
            Div(
                cls="grid",
                children=[
                    Div(
                        cls="card",
                        children=[
                            H2(f"Crew {assignment.crew_id}"),
                            P(f"Assignment ID: {assignment.id}"),
                            Form(
                                Label(
                                    Input(type="checkbox", name="attendance", checked=assignment.attendance_confirmed),
                                    " Attendance Confirmed"
                                ),
                                Label(
                                    Input(type="checkbox", name="ppe_compliance", checked=assignment.ppe_compliance),
                                    " PPE Compliance Confirmed"
                                ),
                                Input(type="hidden", name="assignment_id", value=assignment.id),
                                Button("Submit", type="submit", cls="button"),
                                action="/assignments/attendance",
                                method="post",
                                cls="form"
                            )
                        ]
                    ) for assignment in assignments
                ]
            )
        ]
        return page_view(req, "Attendance & PPE Compliance", content)
    elif req.method == "POST":
        data = await req.form()
        assignment_id = int(data.get("assignment_id"))
        attendance = data.get("attendance") == "on"
        ppe_compliance = data.get("ppe_compliance") == "on"
        assignment = get_assignment_by_id(assignment_id)
        if assignment:
            assignment.mark_attendance(attendance, ppe_compliance)
        return RedirectResponse("/assignments/attendance", status_code=303)