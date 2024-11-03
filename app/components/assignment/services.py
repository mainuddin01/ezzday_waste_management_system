# components/assignment/services.py

from app.components.assignment.models import Assignment

def get_assignments_for_date(assignment_date):
    """Fetches all assignments for a specific date."""
    return Assignment.find_all_for_date(assignment_date)

def get_assignment_by_id(assignment_id):
    """Fetches an assignment by its ID."""
    return Assignment.find_by_id(assignment_id)

def create_assignment(data):
    """Creates a new assignment."""
    new_assignment = Assignment(
        crew_id=int(data.get('crew_id')),
        route_id=int(data.get('route_id')),
        client_id=int(data.get('client_id')),
        zone_id=int(data.get('zone_id')),
        doc=datetime.strptime(data.get('doc'), '%Y-%m-%d').date(),
        week_type=data.get('week_type', 'Regular')
    )
    new_assignment.save()

def update_assignment(assignment_id, data):
    """Updates an existing assignment."""
    assignment = get_assignment_by_id(assignment_id)
    assignment.crew_id = int(data.get('crew_id'))
    assignment.route_id = int(data.get('route_id'))
    assignment.client_id = int(data.get('client_id'))
    assignment.zone_id = int(data.get('zone_id'))
    assignment.doc = datetime.strptime(data.get('doc'), '%Y-%m-%d').date()
    assignment.week_type = data.get('week_type', 'Regular')
    assignment.save()

def delete_assignment(assignment_id):
    """Deletes an existing assignment."""
    assignment = get_assignment_by_id(assignment_id)
    if assignment:
        assignment.delete()