# components/crew/services.py

from app.components.crew.models import Crew

def get_all_crews():
    """Fetches all crews."""
    return Crew.find_all()

def get_crew_by_id(crew_id):
    """Fetches a crew by its ID."""
    return Crew.find_by_id(crew_id)

def create_crew(data):
    """Creates a new crew."""
    loaders = data.getlist('loaders')
    crew = Crew(
        driver_id=int(data.get('driver_id')),
        truck_id=int(data.get('truck_id')),
        loaders=list(map(int, loaders))
    )
    crew.save()

def update_crew(crew_id, data):
    """Updates an existing crew."""
    crew = get_crew_by_id(crew_id)
    if crew:
        loaders = data.getlist('loaders')
        crew.driver_id = int(data.get('driver_id'))
        crew.truck_id = int(data.get('truck_id'))
        crew.loaders = list(map(int, loaders))
        crew.save()

def delete_crew(crew_id):
    """Deletes an existing crew."""
    crew = get_crew_by_id(crew_id)
    if crew:
        crew.delete()