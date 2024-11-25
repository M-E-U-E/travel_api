import unittest
import json
from app import app, users_db
import jwt
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
import coverage

# Start coverage before importing your modules
COV = coverage.coverage(
    branch=True,
    include='app.py',
    omit=[
        'venv/*',
        'tests/*',
        '__init__.py'
    ]
)
COV.start()

class TestUsersAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        
        # Clear users_db
        users_db.clear()
        
        # Add test admin user with hashed password
        admin_password = generate_password_hash("admin123")
        users_db["1"] = {
            "id": "1",
            "username": "admin",
            "password": admin_password,
            "email": "admin@example.com",
            "role": "admin"
        }

    def get_admin_token(self):
        """Helper method to get admin token"""
        response = self.app.post('/login',
            json={
                "username": "admin",
                "password": "admin123"
            },
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertIn('token', data, "Token not found in response")
        return data['token']

    def test_register_success(self):
        """Test successful user registration"""
        response = self.app.post('/register',
            json={
                "username": "testuser",
                "password": "Test123Password",
                "email": "test@example.com",
                "role": "user"
            }
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['user']['username'], 'testuser')
        self.assertEqual(data['user']['email'], 'test@example.com')
        self.assertEqual(data['user']['role'], 'user')

    def test_register_invalid_data(self):
        """Test registration with invalid data"""
        # Test missing fields
        response = self.app.post('/register',
            json={
                "username": "testuser"
            }
        )
        self.assertEqual(response.status_code, 400)

        # Test invalid email
        response = self.app.post('/register',
            json={
                "username": "testuser",
                "password": "Test123Password",
                "email": "invalid-email",
                "role": "user"
            }
        )
        self.assertEqual(response.status_code, 400)

        # Test weak password
        response = self.app.post('/register',
            json={
                "username": "testuser",
                "password": "weak",
                "email": "test@example.com",
                "role": "user"
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_login_success(self):
        """Test successful login"""
        # First register a user
        self.app.post('/register',
            json={
                "username": "testuser",
                "password": "Test123Password",
                "email": "test@example.com",
                "role": "user"
            }
        )

        # Then try to login
        response = self.app.post('/login',
            json={
                "username": "testuser",
                "password": "Test123Password"
            }
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('token', data)
        self.assertIn('user', data)

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = self.app.post('/login',
            json={
                "username": "nonexistent",
                "password": "wrongpassword"
            }
        )
        self.assertEqual(response.status_code, 401)

    def test_get_profile_success(self):
        """Test getting user profile with valid token"""
        # Get admin token
        token = self.get_admin_token()
        
        # Test profile access
        response = self.app.get('/profile',
            headers={
                'Authorization': f'Bearer {token}'
            }
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertEqual(data['username'], 'admin')
        self.assertEqual(data['role'], 'admin')

    def test_get_profile_invalid_token(self):
        """Test getting profile with invalid token"""
        response = self.app.get('/profile',
            headers={
                'Authorization': 'Bearer invalid-token'
            }
        )
        self.assertEqual(response.status_code, 401)

    def test_get_user_profile_admin(self):
        """Test admin accessing other user's profile"""
        # Register a regular user
        register_response = self.app.post('/register',
            json={
                "username": "testuser",
                "password": "Test123Password",
                "email": "test@example.com",
                "role": "user"
            }
        )
        user_data = json.loads(register_response.data.decode())
        user_id = user_data['user']['id']

        # Get admin token
        token = self.get_admin_token()

        # Test admin accessing user profile
        response = self.app.get(f'/profile/{user_id}',
            headers={
                'Authorization': f'Bearer {token}'
            }
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertEqual(data['username'], 'testuser')

    def test_get_user_profile_unauthorized(self):
        """Test user trying to access another user's profile"""
        # Register first user
        response1 = self.app.post('/register',
            json={
                "username": "user1",
                "password": "Test123Password",
                "email": "user1@example.com",
                "role": "user"
            }
        )
        user1_data = json.loads(response1.data.decode())
        user1_id = user1_data['user']['id']

        # Register second user
        response2 = self.app.post('/register',
            json={
                "username": "user2",
                "password": "Test123Password",
                "email": "user2@example.com",
                "role": "user"
            }
        )
        user2_data = json.loads(response2.data.decode())
        user2_id = user2_data['user']['id']

        # Login as first user
        login_response = self.app.post('/login',
            json={
                "username": "user1",
                "password": "Test123Password"
            }
        )
        token = json.loads(login_response.data.decode())['token']

        # Try to access second user's profile
        response = self.app.get(f'/profile/{user2_id}',
            headers={
                'Authorization': f'Bearer {token}'
            }
        )
        self.assertEqual(response.status_code, 401)

    def test_validate_email(self):
        """Test email validation"""
        from app import validate_email
        
        # Valid emails
        self.assertTrue(validate_email('test@example.com'))
        self.assertTrue(validate_email('user.name@domain.co.uk'))
        
        # Invalid emails
        self.assertFalse(validate_email('invalid-email'))
        self.assertFalse(validate_email('@domain.com'))
        self.assertFalse(validate_email('user@'))

    def test_validate_password(self):
        """Test password validation"""
        from app import validate_password
        
        # Valid passwords
        self.assertTrue(validate_password('Test123Password'))
        self.assertTrue(validate_password('SecurePass1'))
        
        # Invalid passwords
        self.assertFalse(validate_password('short1'))  # Too short
        self.assertFalse(validate_password('lowercase1'))  # No uppercase
        self.assertFalse(validate_password('UPPERCASE1'))  # No lowercase
        self.assertFalse(validate_password('NoNumbers'))  # No numbers

    def test_validate_username(self):
        """Test username validation"""
        from app import validate_username
        
        # Valid usernames
        self.assertTrue(validate_username('user123'))
        self.assertTrue(validate_username('User_123'))
        
        # Invalid usernames
        self.assertFalse(validate_username('ab'))  # Too short
        self.assertFalse(validate_username('user@123'))  # Invalid character
        self.assertFalse(validate_username('very_long_username_123456'))  # Too long

    def test_missing_token(self):
        """Test endpoints without token"""
        response = self.app.get('/profile')
        self.assertEqual(response.status_code, 401)
        
        response = self.app.get('/profile/1')
        self.assertEqual(response.status_code, 401)

    def test_invalid_user_id_format(self):
        """Test profile access with invalid user ID format"""
        token = self.get_admin_token()
        
        response = self.app.get('/profile/invalid-uuid',
            headers={
                'Authorization': f'Bearer {token}'
            }
        )
        self.assertEqual(response.status_code, 400)

def run_tests():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('.')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1

if __name__ == '__main__':
    run_tests() 