from flask import Flask, jsonify, request, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
from .utils import validate_token, is_authorized

app = Flask(__name__)
CORS(app)

@app.route('/validate', methods=['POST'])
def validate():
    """
    Validate Token
    ---
    tags:
      - Authorization
    parameters:
      - name: Authorization
        in: header
        required: true
        schema:
          type: string
          description: Bearer token to validate
    responses:
      200:
        description: Token is valid
        content:
          application/json:
            schema:
              type: object
              properties:
                user_id:
                  type: integer
                role:
                  type: string
      401:
        description: Invalid token
    """
    token = request.headers.get('Authorization')
    user_id, role = validate_token(token)
    if user_id and role:
        return jsonify({'user_id': user_id, 'role': role})
    else:
        return jsonify({'error': 'Invalid token'}), 401

@app.route('/authorize', methods=['POST'])
def authorize():
    """
    Check User Authorization
    ---
    tags:
      - Authorization
    parameters:
      - name: Authorization
        in: header
        required: true
        schema:
          type: string
          description: Bearer token for authentication
    requestBody:
      description: Resource to access
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              resource:
                type: string
    responses:
      200:
        description: Authorized
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
      403:
        description: Unauthorized
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
    """
    token = request.headers.get('Authorization')
    resource = request.get_json()['resource']
    role = validate_token(token)[1]
    if is_authorized(role, resource):
        return jsonify({'message': 'Authorized'})
    else:
        return jsonify({'error': 'Unauthorized'}), 403

# Swagger UI setup
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'  # Path to the OpenAPI spec file
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "Authorization API"})

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Serve OpenAPI spec file
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

# Add a route to serve swagger.json
@app.route('/static/swagger.json')
def serve_swagger_spec():
    return jsonify({
        "swagger": "2.0",
        "info": {
            "title": "Authorization API",
            "version": "1.0.0"
        },
        "basePath": "/",
        "schemes": ["http"],
        "paths": {
            "/validate": {
                "post": {
                    "tags": ["Authorization"],
                    "summary": "Validate Token",
                    "parameters": [
                        {
                            "name": "Authorization",
                            "in": "header",
                            "required": True,
                            "type": "string",
                            "description": "Bearer token to validate"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Token is valid",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "user_id": {"type": "string"},
                                    "role": {"type": "string"}
                                }
                            }
                        },
                        "401": {
                            "description": "Invalid token"
                        }
                    }
                }
            },
            "/authorize": {
                "post": {
                    "tags": ["Authorization"],
                    "summary": "Check User Authorization",
                    "parameters": [
                        {
                            "name": "Authorization",
                            "in": "header",
                            "required": True,
                            "type": "string",
                            "description": "Bearer token for authentication"
                        },
                        {
                            "name": "body",
                            "in": "body",
                            "required": True,
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "resource": {"type": "string"}
                                }
                            }
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Authorized",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "message": {"type": "string"}
                                }
                            }
                        },
                        "403": {
                            "description": "Unauthorized"
                        }
                    }
                }
            }
        }
    })

if __name__ == '__main__':
    app.run(debug=True, port=5003)
