destinations = [
    {
        'id': 1,
        'name': 'Paris',
        'description': 'The City of Light',
        'location': 'France',
        'price_per_night': 150.0
    },
    {
        'id': 2,
        'name': 'New York City',
        'description': 'The Big Apple',
        'location': 'USA',
        'price_per_night': 300.0
    }
]

def get_destinations():
    return destinations


def add_destination(data):
    destination = {
        'id': len(destinations) + 1,
        'name': data['name'],
        'description': data['description'],
        'location': data['location'],
        'price_per_night': data['price_per_night']
    }
    destinations.append(destination)
    return destination


def delete_destination(destination_id):
    for i, dest in enumerate(destinations):
        if dest['id'] == destination_id:
            del destinations[i]
            return True
    return False

def is_admin(request):
    # Implement role-based access control logic
    return request.headers.get('X-User-Role') == 'Admin'