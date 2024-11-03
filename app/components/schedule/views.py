# components/schedule/views.py

from fasthtml.common import *
from app.components.schedule.forms import schedule_form
from app.components.schedule.services import (
    create_schedule, update_schedule, delete_schedule
)
from app.components.schedule.models import Schedule
from app.components.driver.services import get_all_drivers
from app.components.loader.services import get_all_loaders
from app.components.common.page import page_view
from starlette.responses import RedirectResponse
from starlette.requests import Request
import logging

logger = logging.getLogger(__name__)

async def schedule_list_view(req: Request):
    """Generates the list view of all schedules."""
    schedules = Schedule.find_all()
    content = [
        H1("Schedules"),
        Table(
            Thead(
                Tr(
                    Th("ID"), Th("Week Number"), Th("Day"), Th("Driver"), Th("Loaders"), Th("Actions")
                )
            ),
            Tbody(
                *[
                    Tr(
                        Td(str(schedule.id)),
                        Td(str(schedule.week_number)),
                        Td(schedule.dow),
                        Td(str(schedule.driver_id)),
                        Td(", ".join(map(str, schedule.loader_ids))),
                        Td(
                            A("Edit", href=f"/schedules/edit/{schedule.id}", cls="button small"),
                            " ",
                            A("Delete", href=f"/schedules/delete/{schedule.id}", cls="button small danger")
                        )
                    ) for schedule in schedules
                ]
            ),
            cls="table-responsive"
        ),
        A("Add New Schedule", href="/schedules/add", cls="button")
    ]
    return page_view(req, "Schedule List", content)

async def schedule_add_view(req: Request):
    """Handles adding a new schedule."""
    drivers = get_all_drivers()
    loaders = get_all_loaders()

    if req.method == "GET":
        content = [
            schedule_form("/schedules/add", drivers=drivers, loaders=loaders)
        ]
        return page_view(req, "Add Schedule", content)
    elif req.method == "POST":
        data = await req.form()
        try:
            create_schedule(data)
            return RedirectResponse("/schedules", status_code=303)
        except ValueError as e:
            logger.error(f"Error creating schedule: {e}")
            content = [
                P(str(e), style="color:red"),
                schedule_form("/schedules/add", drivers=drivers, loaders=loaders)
            ]
            return page_view(req, "Add Schedule", content)

async def schedule_edit_view(req: Request, schedule_id: int):
    """Handles editing an existing schedule."""
    schedule = Schedule.find_by_id(schedule_id)
    if not schedule:
        return page_view(req, "Error", [Div("Schedule not found.")])
    drivers = get_all_drivers()
    loaders = get_all_loaders()

    if req.method == "GET":
        content = [
            schedule_form(f"/schedules/edit/{schedule_id}", schedule=schedule, drivers=drivers, loaders=loaders)
        ]
        return page_view(req, "Edit Schedule", content)
    elif req.method == "POST":
        data = await req.form()
        try:
            update_schedule(schedule_id, data)
            return RedirectResponse("/schedules", status_code=303)
        except ValueError as e:
            logger.error(f"Error updating schedule: {e}")
            content = [
                P(str(e), style="color:red"),
                schedule_form(f"/schedules/edit/{schedule_id}", schedule=schedule, drivers=drivers, loaders=loaders)
            ]
            return page_view(req, "Edit Schedule", content)

async def schedule_delete_view(req: Request, schedule_id: int):
    """Handles deleting an existing schedule."""
    schedule = Schedule.find_by_id(schedule_id)
    if not schedule:
        return page_view(req, "Error", [Div("Schedule not found.")])
    if req.method == "POST":
        delete_schedule(schedule_id)
        return RedirectResponse("/schedules", status_code=303)
    else:
        content = [
            H2(f"Are you sure you want to delete schedule {schedule.id}?"),
            Form(
                Button("Yes, delete", type="submit", cls="button danger"),
                action=f"/schedules/delete/{schedule_id}",
                method="post"
            )
        ]
        return page_view(req, "Delete Schedule", content)