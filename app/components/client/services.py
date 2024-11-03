# app/components/client/services.py

from app.components.client.models import Client

def get_all_clients():
    """Fetches all clients from the database."""
    return Client.find_all()

def get_client_by_id(client_id):
    """Fetches a client by its ID."""
    return Client.find_by_id(client_id)

def create_client(data):
    """Creates a new client."""
    zones_serviced = data.getlist('zones_serviced')  # Assuming data is a MultiDict
    client = Client(
        name=data.get('name'),
        client_type=data.get('client_type'),
        description=data.get('description', ""),
        contact_name=data.get('contact_name'),
        contact_phone=data.get('contact_phone'),
        contact_email=data.get('contact_email'),
        zones_serviced=list(map(int, zones_serviced))
    )
    client.save()

def update_client(client_id, data):
    """Updates an existing client."""
    client = get_client_by_id(client_id)
    zones_serviced = data.getlist('zones_serviced')
    client.name = data.get('name')
    client.client_type = data.get('client_type')
    client.description = data.get('description', "")
    client.contact_name = data.get('contact_name')
    client.contact_phone = data.get('contact_phone')
    client.contact_email = data.get('contact_email')
    client.zones_serviced = list(map(int, zones_serviced))
    client.save()

def delete_client(client_id):
    """Deletes an existing client."""
    client = get_client_by_id(client_id)
    if client:
        client.delete()