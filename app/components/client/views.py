# components/client/views.py

from fasthtml.common import *
from app.components.client.forms import client_form
from app.components.client.services import (
    get_all_clients, get_client_by_id, create_client, update_client, delete_client
)
from app.components.common.page import page_view
from starlette.responses import RedirectResponse
from starlette.requests import Request

async def client_list_view(req: Request):
    """Generates the client list view."""
    clients = get_all_clients()
    content = [
        H1("Clients"),
        Table(
            Thead(
                Tr(
                    Th("ID"), Th("Name"), Th("Type"), Th("Actions")
                )
            ),
            Tbody(
                *[
                    Tr(
                        Td(str(client.id)),
                        Td(client.name),
                        Td(client.client_type),
                        Td(
                            A("Edit", href=f"/clients/edit/{client.id}", cls="button small"),
                            " ",
                            A("Delete", href=f"/clients/delete/{client.id}", cls="button small danger")
                        )
                    ) for client in clients
                ]
            ),
            cls="table-responsive"
        ),
        A("Add New Client", href="/clients/add", cls="button")
    ]
    return page_view(req, "Client List", content)

async def client_add_view(req: Request):
    """Handles adding a new client."""
    if req.method == "GET":
        content = [
            client_form("/clients/add")
        ]
        return page_view(req, "Add Client", content)
    elif req.method == "POST":
        data = await req.form()
        create_client(data)
        return RedirectResponse("/clients", status_code=303)

async def client_edit_view(req: Request, client_id: int):
    """Handles editing an existing client."""
    client = get_client_by_id(client_id)
    if not client:
        return page_view(req, "Error", [Div("Client not found.")])

    if req.method == "GET":
        content = [
            client_form(f"/clients/edit/{client_id}", client=client)
        ]
        return page_view(req, "Edit Client", content)
    elif req.method == "POST":
        data = await req.form()
        update_client(client_id, data)
        return RedirectResponse("/clients", status_code=303)

async def client_delete_view(req: Request, client_id: int):
    """Handles deleting an existing client."""
    client = get_client_by_id(client_id)
    if not client:
        return page_view(req, "Error", [Div("Client not found.")])

    if req.method == "POST":
        delete_client(client_id)
        return RedirectResponse("/clients", status_code=303)
    else:
        content = [
            H2(f"Are you sure you want to delete {client.name}?"),
            Form(
                Button("Yes, delete", type="submit", cls="button danger"),
                action=f"/clients/delete/{client_id}",
                method="post"
            )
        ]
        return page_view(req, "Delete Client", content)