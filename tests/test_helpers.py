import json


def get_token(app, username, password):
    """Helper method to log in and retrieve a token"""
    response = app.post('/login', json={"username": username, "password": password})
    data = json.loads(response.data)
    return data.get('token')
