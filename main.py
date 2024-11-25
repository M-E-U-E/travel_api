from flask import Flask, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from destinations.app import app as destinations_app
from users.app import app as users_app
from authentication.app import app as authentication_app
app = Flask(__name__)

# Swagger setup
SWAGGER_URL = '/docs'  # URL for swagger documentation
API_URL = '/swagger.json'  # URL for swagger.json

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Travel API"
    }
)

# Register blueprint
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/swagger.json')
def swagger_json():
    return send_file('static/swagger.json')

# Add some routes to make the swagger doc more meaningful
@app.route('/auth/login', methods=['POST'])
def login():
    return jsonify({"message": "Login endpoint"})

@app.route('/destinations', methods=['GET', 'POST'])
def destinations():
    return jsonify({"message": "Destinations endpoint"})

@app.route('/users', methods=['GET', 'POST'])
def users():
    return jsonify({"message": "Users endpoint"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    destinations_app.run(port=5001)
    users_app.run(port=5002)
    authentication_app.run(port=5003)