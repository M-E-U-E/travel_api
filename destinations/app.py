from flask import Flask, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
from functools import wraps
import requests

app = Flask(__name__)
CORS(app)

# Sample destinations data
destinations = [
    {
        "id": 1,
        "name": "Paris",
        "description": "The city of lights",
        "location": "France"
    },
    {
        "id": 2,
        "name": "Tokyo",
        "description": "A bustling metropolis",
        "location": "Japan"
    },
    {
        "id": 3,
        "name": "New York",
        "description": "The city that never sleeps",
        "location": "USA"
    },
    {
        "id": 4,
        "name": "Sydney",
        "description": "Home to the iconic Opera House",
        "location": "Australia"
    },
    {
        "id": 5,
        "name": "Rome",
        "description": "The Eternal City with a rich history",
        "location": "Italy"
    },
    {
        "id": 6,
        "name": "Cairo",
        "description": "The land of the ancient pyramids",
        "location": "Egypt"
    },
    {
        "id": 7,
        "name": "Cape Town",
        "description": "A stunning coastal city",
        "location": "South Africa"
    },
    {
        "id": 8,
        "name": "Bangkok",
        "description": "The vibrant capital of Thailand",
        "location": "Thailand"
    },
    {
        "id": 9,
        "name": "Rio de Janeiro",
        "description": "Famous for its Carnival and beaches",
        "location": "Brazil"
    },
    {
        "id": 10,
        "name": "Istanbul",
        "description": "Where East meets West",
        "location": "Turkey"
    }
]

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token is missing'}), 401

        try:
            # Validate token with authentication service
            response = requests.post(
                'http://localhost:5003/validate',
                headers={'Authorization': token}
            )
            
            if response.status_code != 200:
                return jsonify({'error': 'Invalid token'}), 401
                
            user_data = response.json()
            return f(user_data, *args, **kwargs)
            
        except requests.RequestException:
            return jsonify({'error': 'Authentication service unavailable'}), 503
            
    return decorated

@app.route('/destinations', methods=['GET'])
def get_destinations():
    return jsonify(destinations)

@app.route('/destinations/<int:destination_id>', methods=['DELETE'])
@token_required
def delete_destination(user_data, destination_id):
    if user_data.get('role') != 'admin':
        return jsonify({'error': 'Admin access required'}), 403
        
    destination = next((d for d in destinations if d['id'] == destination_id), None)
    if not destination:
        return jsonify({'error': 'Destination not found'}), 404
        
    destinations.remove(destination)
    return jsonify({'message': f'Destination {destination_id} deleted successfully'})

@app.route('/swagger.json')
def swagger_spec():
    return jsonify({
        "openapi": "3.0.0",
        "info": {
            "title": "Destinations API",
            "description": "API for managing travel destinations",
            "version": "1.0.0"
        },
        "servers": [
            {
                "url": "http://localhost:5002",
                "description": "Development server"
            }
        ],
        "components": {
            "securitySchemes": {
                "bearerAuth": {
                    "type": "apiKey",
                    "name": "Authorization",
                    "in": "header",
                    "description": "Enter your token with Bearer prefix. Example: Bearer eyJhbGc..."
                }
            }
        },
        "security": [
            {
                "bearerAuth": []
            }
        ],
        "paths": {
            "/destinations": {
                "get": {
                    "tags": ["Destinations"],
                    "summary": "List all destinations",
                    "security": [],  # No security for GET
                    "responses": {
                        "200": {
                            "description": "List of destinations",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "id": {"type": "integer"},
                                                "name": {"type": "string"},
                                                "description": {"type": "string"},
                                                "location": {"type": "string"}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/destinations/{destination_id}": {
                "delete": {
                    "tags": ["Destinations"],
                    "summary": "Delete a destination (Admin only)",
                    "security": [
                        {
                            "bearerAuth": []
                        }
                    ],
                    "parameters": [
                        {
                            "name": "destination_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "integer"},
                            "description": "ID of destination to delete"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Destination deleted successfully",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "message": {"type": "string"}
                                        }
                                    }
                                }
                            }
                        },
                        "401": {
                            "description": "Unauthorized - Token missing or invalid"
                        },
                        "403": {
                            "description": "Forbidden - Admin access required"
                        },
                        "404": {
                            "description": "Destination not found"
                        }
                    }
                }
            }
        }
    })

# Swagger UI configuration
SWAGGER_URL = '/swagger'
API_URL = '/swagger.json'

swagger_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Destinations API",
        'persistAuthorization': True,
        'displayOperationId': True,
        'docExpansion': 'list',
        'defaultModelsExpandDepth': -1
    }
)

app.register_blueprint(swagger_blueprint, url_prefix=SWAGGER_URL)

if __name__ == '__main__':
    app.run(debug=True, port=5002)
