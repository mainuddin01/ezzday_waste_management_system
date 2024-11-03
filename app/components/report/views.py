# components/report/views.py

from fasthtml.common import *
from app.components.report.forms import report_form
from app.components.report.services import generate_report
from app.components.report.models import Report
from app.components.common.page import page_view
from starlette.responses import RedirectResponse, FileResponse
from starlette.requests import Request
import json
import os
import logging

logger = logging.getLogger(__name__)

async def report_list_view(req: Request):
    """Generates the list view of all reports."""
    reports = Report.find_all()
    content = [
        H1("Generated Reports"),
        Table(
            Thead(
                Tr(
                    Th("ID"), Th("Report Type"), Th("Generated At"), Th("Actions")
                )
            ),
            Tbody(
                *[
                    Tr(
                        Td(str(report.id)),
                        Td(report.report_type),
                        Td(report.generated_at.strftime('%Y-%m-%d %H:%M:%S')),
                        Td(
                            A("View", href=f"/reports/view/{report.id}", cls="button small"),
                            " ",
                            A("Download", href=f"/reports/download/{report.id}", cls="button small"),
                            " ",
                            A("Delete", href=f"/reports/delete/{report.id}", cls="button small danger")
                        )
                    ) for report in reports
                ]
            ),
            cls="table-responsive"
        ),
        A("Generate New Report", href="/reports/generate", cls="button")
    ]
    return page_view(req, "Report List", content)

async def generate_report_view(req: Request):
    """Handles report generation and rendering."""
    if req.method == "GET":
        content = [
            report_form("/reports/generate")
        ]
        return page_view(req, "Generate Report", content)
    elif req.method == "POST":
        data = await req.form()
        report_type = data.get('report_type')
        parameters_str = data.get('parameters', '{}')
        try:
            parameters = json.loads(parameters_str)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON parameters: {e}")
            content = [
                P("Invalid JSON format in parameters.", style="color:red"),
                report_form("/reports/generate")
            ]
            return page_view(req, "Generate Report", content)
        try:
            report = generate_report(report_type, parameters)
            return RedirectResponse(f"/reports/view/{report.id}", status_code=303)
        except ValueError as e:
            logger.error(f"Error generating report: {e}")
            content = [
                P(str(e), style="color:red"),
                report_form("/reports/generate")
            ]
            return page_view(req, "Generate Report", content)

async def view_report_view(req: Request, report_id: int):
    """Handles viewing a specific report."""
    report = Report.find_by_id(report_id)
    if not report:
        return page_view(req, "Error", [P("Report not found.")])
    content = [
        H1(f"Report: {report.report_type}"),
        P(f"Generated At: {report.generated_at.strftime('%Y-%m-%d %H:%M:%S')}"),
        Pre(f"Parameters:\n{json.dumps(report.parameters, indent=2)}"),
        A("Download Report", href=f"/reports/download/{report.id}", cls="button"),
        A("Delete Report", href=f"/reports/delete/{report.id}", cls="button danger")
    ]
    return page_view(req, f"View Report - {report.report_type}", content)

async def download_report_view(req: Request, report_id: int):
    """Handles downloading a report file."""
    report = Report.find_by_id(report_id)
    if not report or not os.path.exists(report.file_path):
        return page_view(req, "Error", [P("Report file not found.")])
    return FileResponse(
        path=report.file_path,
        filename=os.path.basename(report.file_path),
        media_type='application/octet-stream'
    )

async def delete_report_view(req: Request, report_id: int):
    """Handles deleting a report."""
    report = Report.find_by_id(report_id)
    if not report:
        return page_view(req, "Error", [Div("Report not found.")])
    if req.method == "POST":
        # Delete the report file
        if os.path.exists(report.file_path):
            os.remove(report.file_path)
        report.delete()
        return RedirectResponse("/reports", status_code=303)
    else:
        content = [
            H2(f"Are you sure you want to delete report {report.report_type}?"),
            Form(
                Button("Yes, delete", type="submit", cls="button danger"),
                action=f"/reports/delete/{report_id}",
                method="post"
            )
        ]
        return page_view(req, "Delete Report", content)