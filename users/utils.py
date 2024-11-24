import hashlib
import jwt

users = [
    {
        'id': 1,
        'name': 'John Doe',
        'email': 'john@example.com',
        'password': hashlib.sha256('password'.encode()).hexdigest(),
        'role': 'Admin'
    },
    {
        'id': 2,
        'name': 'Jane Smith',
        'email': 'jane@example.com',
        'password': hashlib.sha256('password123'.encode()).hexdigest(),
        'role': 'User'
    }
]

def register_user(data):
    user = {
        'id': len(users) + 1,
        'name': data['name'],
        'email': data['email'],
        'password': hashlib.sha256(data['password'].encode()).hexdigest(),
        'role': 'User'
    }
    users.append(user)
    return user

def login_user(data):
    for user in users:
        if user['email'] == data['email'] and user['password'] == hashlib.sha256(data['password'].encode()).hexdigest():
            return jwt.encode({'user_id': user['id'], 'role': user['role']}, 'secret_key', algorithm='HS256')
    return None

def get_user_profile(token):
    try:
        payload = jwt.decode(token, 'secret_key', algorithms=['HS256'])
        for user in users:
            if user['id'] == payload['user_id']:
                return user
    except jwt.exceptions.InvalidTokenError:
        return None