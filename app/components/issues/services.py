# components/issues/services.py

from app.components.issues.models import Issue
from datetime import datetime
from typing import List

def get_all_issues() -> List[Issue]:
    """Fetches all issues."""
    return Issue.find_all()

def get_issue_by_id(issue_id: int) -> Issue:
    """Fetches an issue by its ID."""
    return Issue.find_by_id(issue_id)

def create_issue(data):
    """
    Creates a new issue.
    Raises:
        ValueError: If validation fails.
    """
    try:
        crew_id = int(data['crew_id'])
        route_id = int(data['route_id'])
        address = data['address']
        issue_type = data['issue_type']
        description = data.get('description', '')
        date_reported_str = data.get('date_reported', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        date_reported = datetime.strptime(date_reported_str, "%Y-%m-%d %H:%M:%S")
    except (ValueError, KeyError) as e:
        raise ValueError("Invalid input data.") from e

    if not address or not issue_type:
        raise ValueError("Address and Issue Type are required.")

    new_issue = Issue(
        crew_id=crew_id,
        route_id=route_id,
        address=address,
        description=description,
        issue_type=issue_type,
        date_reported=date_reported
    )
    new_issue.save()

def update_issue(issue_id: int, data):
    """
    Updates an existing issue.
    Raises:
        ValueError: If validation fails.
    """
    issue = get_issue_by_id(issue_id)
    if not issue:
        raise ValueError("Issue not found.")

    try:
        crew_id = int(data['crew_id'])
        route_id = int(data['route_id'])
        address = data['address']
        issue_type = data['issue_type']
        description = data.get('description', '')
        date_reported_str = data.get('date_reported', issue.date_reported.strftime("%Y-%m-%d %H:%M:%S"))
        date_reported = datetime.strptime(date_reported_str, "%Y-%m-%d %H:%M:%S")
    except (ValueError, KeyError) as e:
        raise ValueError("Invalid input data.") from e

    if not address or not issue_type:
        raise ValueError("Address and Issue Type are required.")

    issue.crew_id = crew_id
    issue.route_id = route_id
    issue.address = address
    issue.description = description
    issue.issue_type = issue_type
    issue.date_reported = date_reported
    issue.save()

def delete_issue(issue_id: int):
    """Deletes an existing issue."""
    issue = get_issue_by_id(issue_id)
    if issue:
        issue.delete()