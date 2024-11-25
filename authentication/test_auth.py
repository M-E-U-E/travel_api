import unittest
import json
import jwt
from datetime import datetime, timedelta
from app import app
from .utils import validate_token, is_authorized

class TestAuthAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.secret_key = 'your-secret-key'

    def create_token(self, username='testuser', role='user', expired=False):
        """Helper method to create test tokens"""
        payload = {
            'username': username,
            'role': role,
            'exp': datetime.utcnow() + timedelta(hours=-1 if expired else 24)
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')

    def test_validate_valid_token(self):
        """Test token validation with valid token"""
        token = self.create_token(role='admin')
        response = self.app.post('/validate',
            headers={'Authorization': f'Bearer {token}'}
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertIn('role', data)
        self.assertEqual(data['role'], 'admin')

    def test_validate_expired_token(self):
        """Test token validation with expired token"""
        token = self.create_token(expired=True)
        response = self.app.post('/validate',
            headers={'Authorization': f'Bearer {token}'}
        )
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data.decode())
        self.assertIn('error', data)

    def test_validate_invalid_token(self):
        """Test token validation with invalid token"""
        response = self.app.post('/validate',
            headers={'Authorization': 'Bearer invalid-token'}
        )
        self.assertEqual(response.status_code, 401)

    def test_validate_missing_token(self):
        """Test token validation without token"""
        response = self.app.post('/validate')
        self.assertEqual(response.status_code, 401)

    def test_authorize_admin_access(self):
        """Test authorization for admin role"""
        token = self.create_token(role='admin')
        response = self.app.post('/authorize',
            headers={'Authorization': f'Bearer {token}'},
            json={'resource': 'any_resource'}
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertEqual(data['message'], 'Authorized')

    def test_authorize_user_access(self):
        """Test authorization for user role"""
        token = self.create_token(role='user')
        response = self.app.post('/authorize',
            headers={'Authorization': f'Bearer {token}'},
            json={'resource': 'view_destinations'}
        )
        self.assertEqual(response.status_code, 200)

    def test_authorize_unauthorized_access(self):
        """Test authorization with insufficient permissions"""
        token = self.create_token(role='user')
        response = self.app.post('/authorize',
            headers={'Authorization': f'Bearer {token}'},
            json={'resource': 'admin_only_resource'}
        )
        self.assertEqual(response.status_code, 403)

    def test_authorize_missing_resource(self):
        """Test authorization without resource"""
        token = self.create_token()
        response = self.app.post('/authorize',
            headers={'Authorization': f'Bearer {token}'},
            json={}
        )
        self.assertEqual(response.status_code, 400)

    def test_authorize_invalid_json(self):
        """Test authorization with invalid JSON"""
        token = self.create_token()
        response = self.app.post('/authorize',
            headers={
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            },
            data='invalid json'
        )
        self.assertEqual(response.status_code, 400)

    def test_swagger_ui_access(self):
        """Test access to Swagger UI"""
        response = self.app.get('/swagger/')
        self.assertEqual(response.status_code, 200)

    def test_swagger_json_access(self):
        """Test access to swagger.json"""
        response = self.app.get('/static/swagger.json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertEqual(data['info']['title'], 'Authorization API')

    def test_utils_validate_token(self):
        """Test token validation utility function"""
        # Valid token
        token = self.create_token(username='testuser', role='admin')
        username, role = validate_token(f'Bearer {token}')
        self.assertEqual(username, 'testuser')
        self.assertEqual(role, 'admin')

        # Invalid token
        username, role = validate_token('invalid-token')
        self.assertIsNone(username)
        self.assertIsNone(role)

    def test_utils_is_authorized(self):
        """Test authorization utility function"""
        # Admin role
        self.assertTrue(is_authorized('admin', 'any_resource'))
        
        # User role with allowed resource
        self.assertTrue(is_authorized('user', 'view_destinations'))
        
        # User role with restricted resource
        self.assertFalse(is_authorized('user', 'admin_resource'))
        
        # Invalid role
        self.assertFalse(is_authorized('invalid_role', 'any_resource'))

if __name__ == '__main__':
    import coverage
    
    # Start coverage reporting
    cov = coverage.Coverage()
    cov.start()
    
    # Run tests
    unittest.main(exit=False)
    
    # Stop coverage
    cov.stop()
    cov.save()
    
    # Report coverage
    print('\nCoverage Summary:')
    cov.report()
    
    # Generate HTML report
    cov.html_report(directory='coverage_report') 