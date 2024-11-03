# components/loader/views.py

from fasthtml.common import *
from app.components.loader.forms import loader_form
from app.components.loader.services import (
    get_all_loaders, get_loader_by_id, create_loader, update_loader, delete_loader
)
from app.components.common.page import page_view
from starlette.responses import RedirectResponse
from starlette.requests import Request
import logging

logger = logging.getLogger(__name__)

async def loader_list_view(req: Request):
    """Generates the loader list view."""
    loaders = get_all_loaders()
    content = [
        H1("Loaders"),
        Table(
            Thead(
                Tr(
                    Th("ID"), Th("Name"), Th("Employee ID"), Th("Actions")
                )
            ),
            Tbody(
                *[
                    Tr(
                        Td(str(loader.id)),
                        Td(loader.name),
                        Td(loader.employee_id),
                        Td(
                            A("Edit", href=f"/loaders/edit/{loader.id}", cls="button small"),
                            " ",
                            A("Delete", href=f"/loaders/delete/{loader.id}", cls="button small danger")
                        )
                    ) for loader in loaders
                ]
            ),
            cls="table-responsive"
        ),
        A("Add New Loader", href="/loaders/add", cls="button")
    ]
    return page_view(req, "Loader List", content)

async def loader_add_view(req: Request):
    """Handles adding a new loader."""
    if req.method == "GET":
        content = [
            loader_form("/loaders/add")
        ]
        return page_view(req, "Add Loader", content)
    elif req.method == "POST":
        data = await req.form()
        try:
            create_loader(data)
            return RedirectResponse("/loaders", status_code=303)
        except ValueError as e:
            logger.error(f"Error creating loader: {e}")
            content = [
                P(str(e), style="color:red"),
                loader_form("/loaders/add")
            ]
            return page_view(req, "Add Loader", content)

async def loader_edit_view(req: Request, loader_id: int):
    """Handles editing an existing loader."""
    loader = get_loader_by_id(loader_id)
    if not loader:
        return page_view(req, "Error", [Div("Loader not found.")])

    if req.method == "GET":
        content = [
            loader_form(f"/loaders/edit/{loader_id}", loader=loader)
        ]
        return page_view(req, "Edit Loader", content)
    elif req.method == "POST":
        data = await req.form()
        try:
            update_loader(loader_id, data)
            return RedirectResponse("/loaders", status_code=303)
        except ValueError as e:
            logger.error(f"Error updating loader: {e}")
            content = [
                P(str(e), style="color:red"),
                loader_form(f"/loaders/edit/{loader_id}", loader=loader)
            ]
            return page_view(req, "Edit Loader", content)

async def loader_delete_view(req: Request, loader_id: int):
    """Handles deleting an existing loader."""
    loader = get_loader_by_id(loader_id)
    if not loader:
        return page_view(req, "Error", [Div("Loader not found.")])

    if req.method == "POST":
        delete_loader(loader_id)
        return RedirectResponse("/loaders", status_code=303)
    else:
        content = [
            H2(f"Are you sure you want to delete loader {loader.name}?"),
            Form(
                Button("Yes, delete", type="submit", cls="button danger"),
                action=f"/loaders/delete/{loader_id}",
                method="post"
            )
        ]
        return page_view(req, "Delete Loader", content)