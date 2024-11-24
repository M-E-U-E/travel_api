from flask import Flask, jsonify, request, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
import uuid
import requests
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Change this in production

# In-memory storage (replace with a proper database in production)
users_db = {
    "1": {
        "id": "1",
        "username": "admin",
        "password": generate_password_hash("admin123"),  # Using werkzeug instead of bcrypt
        "email": "admin@example.com",
        "role": "admin"
    }
}

def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))

def validate_password(password):
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    return True

def validate_username(username):
    return bool(re.match(r'^[a-zA-Z0-9_]{3,20}$', username))

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        # Debug print
        print("Received token:", token)  # For debugging
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
            
        try:
            # Handle 'Bearer ' prefix
            if token.startswith('Bearer '):
                token = token.split(' ')[1]
                
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = users_db.get(data['username'])
            
            if not current_user:
                return jsonify({'error': 'User not found'}), 404
                
            return f(current_user, *args, **kwargs)
            
        except Exception as e:
            print("Token error:", str(e))  # For debugging
            return jsonify({'error': 'Invalid token'}), 401
            
    return decorated

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    required_fields = ['username', 'password', 'email']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400
    
    if not validate_username(data['username']):
        return jsonify({'error': 'Invalid username. Must be 3-20 characters, alphanumeric and underscore only'}), 400
    
    if not validate_password(data['password']):
        return jsonify({'error': 'Invalid password. Must be at least 8 characters with 1 uppercase, 1 lowercase, and 1 number'}), 400
    
    if not validate_email(data['email']):
        return jsonify({'error': 'Invalid email format'}), 400

    role = data.get('role', 'user')
    if role not in ['user', 'admin']:
        return jsonify({'error': 'Invalid role. Must be either "user" or "admin"'}), 400

    if any(user['username'] == data['username'] for user in users_db.values()):
        return jsonify({'error': 'Username already exists'}), 400
    
    if any(user['email'] == data['email'] for user in users_db.values()):
        return jsonify({'error': 'Email already exists'}), 400

    user_id = str(uuid.uuid4())
    
    hashed_password = generate_password_hash(data['password'])
    
    new_user = {
        'id': user_id,
        'username': data['username'],
        'password': hashed_password,
        'email': data['email'],
        'role': role
    }
    
    users_db[user_id] = new_user
    
    return jsonify({
        'message': 'User registered successfully',
        'user': {
            'id': user_id,
            'username': data['username'],
            'email': data['email'],
            'role': role
        }
    }), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    required_fields = ['username', 'password']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400
    
    if not validate_username(data['username']):
        return jsonify({'error': 'Invalid username format'}), 400

    user = None
    for u in users_db.values():
        if u['username'] == data['username']:
            user = u
            break

    if not user or not check_password_hash(user['password'], data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401

    token = jwt.encode({
        'username': user['username'],
        'role': user['role'],
        'exp': datetime.utcnow() + timedelta(hours=24)
    }, app.config['SECRET_KEY'], algorithm='HS256')

    return jsonify({
        'token': token,
        'user': {
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'role': user['role']
        }
    })

@app.route('/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    return jsonify({
        'id': current_user['id'],
        'username': current_user['username'],
        'email': current_user['email'],
        'role': current_user['role']
    })

@app.route('/profile/<user_id>', methods=['GET'])
@token_required
def get_user_profile(current_user, user_id):
    try:
        uuid.UUID(str(user_id))
    except ValueError:
        return jsonify({'error': 'Invalid user ID format'}), 400

    if current_user['role'] != 'admin' and current_user['id'] != user_id:
        return jsonify({'error': 'Unauthorized access'}), 401

    user = users_db.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({
        'id': user['id'],
        'username': user['username'],
        'email': user['email'],
        'role': user['role']
    })

# Swagger UI configuration
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swagger_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "User Management API",
        'specs_route': "/static/swagger.json"
    }
)
app.register_blueprint(swagger_blueprint, url_prefix=SWAGGER_URL)

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    # Add default admin user
    admin_password = generate_password_hash("admin123")
    users_db["admin"] = {
        "id": "1",
        "username": "admin",
        "password": admin_password,
        "email": "admin@example.com",
        "role": "admin"
    }
    app.run(debug=True, port=5001)