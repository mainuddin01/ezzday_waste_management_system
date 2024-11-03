# components/common/page.py

from fasthtml.common import *
from app.components.common.base import base_component

def page_view(req, page_title, body_content):
    """Renders a generic page with a title and body content."""
    content = [
        Div(
            cls="container",
            *[
                H1(page_title),
                Div(
                    cls="page-content",
                    *body_content
                )
            ]
        )
    ]
    return base_component(page_title, content, req)