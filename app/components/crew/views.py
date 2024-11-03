# components/crew/views.py

from fasthtml.common import *
from app.components.crew.forms import crew_form
from app.components.crew.services import (
    get_all_crews, get_crew_by_id, create_crew, update_crew, delete_crew
)
from app.components.common.page import page_view
from starlette.responses import RedirectResponse
from starlette.requests import Request

async def crew_list_view(req: Request):
    """Generates the crew list view."""
    crews = get_all_crews()
    content = [
        H1("Crews"),
        Table(
            Thead(
                Tr(
                    Th("ID"), Th("Driver"), Th("Loaders"), Th("Actions")
                )
            ),
            Tbody(
                *[
                    Tr(
                        Td(str(crew.id)),
                        Td(str(crew.driver_id)),
                        Td(", ".join(map(str, crew.loader_ids))),
                        Td(
                            A("Edit", href=f"/crews/edit/{crew.id}", cls="button small"),
                            " ",
                            A("Delete", href=f"/crews/delete/{crew.id}", cls="button small danger")
                        )
                    ) for crew in crews
                ]
            ),
            cls="table-responsive"
        ),
        A("Add New Crew", href="/crews/add", cls="button")
    ]
    return page_view(req, "Crew List", content)

async def crew_add_view(req: Request):
    """Handles adding a new crew."""
    if req.method == "GET":
        content = [
            crew_form("/crews/add")
        ]
        return page_view(req, "Add Crew", content)
    elif req.method == "POST":
        data = await req.form()
        create_crew(data)
        return RedirectResponse("/crews", status_code=303)

async def crew_edit_view(req: Request, crew_id: int):
    """Handles editing an existing crew."""
    crew = get_crew_by_id(crew_id)
    if not crew:
        return page_view(req, "Error", [Div("Crew not found.")])

    if req.method == "GET":
        content = [
            crew_form(f"/crews/edit/{crew_id}", crew=crew)
        ]
        return page_view(req, "Edit Crew", content)
    elif req.method == "POST":
        data = await req.form()
        update_crew(crew_id, data)
        return RedirectResponse("/crews", status_code=303)

async def crew_delete_view(req: Request, crew_id: int):
    """Handles deleting an existing crew."""
    crew = get_crew_by_id(crew_id)
    if not crew:
        return page_view(req, "Error", [Div("Crew not found.")])

    if req.method == "POST":
        delete_crew(crew_id)
        return RedirectResponse("/crews", status_code=303)
    else:
        content = [
            H2(f"Are you sure you want to delete crew {crew.id}?"),
            Form(
                Button("Yes, delete", type="submit", cls="button danger"),
                action=f"/crews/delete/{crew_id}",
                method="post"
            )
        ]
        return page_view(req, "Delete Crew", content)