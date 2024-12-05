# import sys
# import os
# import unittest
# import json
# import jwt
# from datetime import datetime, timedelta
# from unittest.mock import patch

# # Add the project root directory to the Python path
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# # Import app and utils
# from app import app
# from utils import validate_token, is_authorized


# class TestAuthAPI(unittest.TestCase):
#     def setUp(self):
#         """Set up the test client and configuration."""
#         self.app = app.test_client()
#         self.app.testing = True
#         self.secret_key = app.config.get('SECRET_KEY', 'default-secret-key')

#     def create_token(self, username='testuser', role='user', expired=False):
#         """Helper method to create test tokens."""
#         if role not in ['user', 'admin']:
#             raise ValueError(f"Invalid role: {role}")
#         payload = {
#             'username': username,
#             'role': role,
#             'exp': datetime.utcnow() + timedelta(hours=-1 if expired else 24)
#         }
#         return jwt.encode(payload, self.secret_key, algorithm='HS256')

#     # --- Test Cases ---

#     def test_authorize_user_access(self):
#         """Test user role access to allowed resources."""
#         token = self.create_token(role='user')
#         response = self.app.post('/authorize',
#                                  headers={'Authorization': f'Bearer {token}'},
#                                  json={'resource': 'view_destinations'})
#         self.assertEqual(response.status_code, 200)

#     def test_authorize_insufficient_permissions(self):
#         """Test user role trying to access restricted resources."""
#         token = self.create_token(role='user')
#         response = self.app.post('/authorize',
#                                  headers={'Authorization': f'Bearer {token}'},
#                                  json={'resource': 'admin_only_resource'})
#         self.assertEqual(response.status_code, 403)

#     def test_authorize_missing_resource(self):
#         """Test authorization without specifying a resource."""
#         token = self.create_token()
#         response = self.app.post('/authorize',
#                                  headers={'Authorization': f'Bearer {token}'},
#                                  json={})
#         self.assertEqual(response.status_code, 400)

#     def test_authorize_invalid_json(self):
#         """Test authorization with invalid JSON format."""
#         token = self.create_token()
#         response = self.app.post('/authorize',
#                                  headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'},
#                                  data='{"resource":}')  # Invalid JSON
#         self.assertEqual(response.status_code, 400)

#     def test_utils_validate_token(self):
#         """Test token validation utility function."""
#         # Valid token
#         token = self.create_token(username='testuser', role='admin')
#         username, role = validate_token(f'Bearer {token}')
#         self.assertEqual(username, 'testuser')
#         self.assertEqual(role, 'admin')

#         # Invalid token
#         username, role = validate_token('invalid-token')
#         self.assertIsNone(username)
#         self.assertIsNone(role)

#     def test_utils_is_authorized(self):
#         """Test authorization utility function."""
#         # Admin role
#         self.assertTrue(is_authorized('admin', 'any_resource'))
#         # User role with allowed resource
#         self.assertTrue(is_authorized('user', 'view_destinations'))
#         # User role with restricted resource
#         self.assertFalse(is_authorized('user', 'admin_only_resource'))
#         # Invalid role
#         self.assertFalse(is_authorized('invalid_role', 'any_resource'))

#     def test_create_token_with_invalid_role(self):
#         """Test token creation with an invalid role."""
#         with self.assertRaises(ValueError):
#             self.create_token(role='invalid_role')

#     def test_authorize_token_expired(self):
#         """Test authorization with an expired token."""
#         token = self.create_token(expired=True)
#         response = self.app.post('/authorize',
#                                  headers={'Authorization': f'Bearer {token}'},
#                                  json={'resource': 'view_destinations'})
#         self.assertEqual(response.status_code, 401)

#     def test_swagger_ui_access(self):
#         """Test access to Swagger UI."""
#         response = self.app.get('/swagger/')
#         self.assertEqual(response.status_code, 200)

#     def test_swagger_json_access(self):
#         """Test access to swagger.json."""
#         response = self.app.get('/static/swagger.json')
#         self.assertEqual(response.status_code, 200)
#         data = json.loads(response.data.decode())
#         self.assertEqual(data['info']['title'], 'Authorization API')


# if __name__ == '__main__':
#     import coverage

#     # Start coverage reporting
#     cov = coverage.Coverage()
#     cov.start()

#     # Run tests
#     unittest.main(exit=False)

#     # Stop coverage
#     cov.stop()
#     cov.save()

#     # Report coverage
#     print('\nCoverage Summary:')
#     cov.report()

#     # Generate HTML report
#     cov.html_report(directory='coverage_report')
import unittest
import json
from app import app


class TestAuth(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_register_success(self):
        payload = {
            "username": "newuser",
            "password": "StrongPass123",
            "email": "newuser@example.com",
            "role": "user"
        }
        response = self.app.post('/register', json=payload)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'User registered successfully')

    def test_login_success(self):
        payload = {
            "username": "admin",
            "password": "admin123"
        }
        response = self.app.post('/login', json=payload)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('token', data)


if __name__ == '__main__':
    unittest.main()
