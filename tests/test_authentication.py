import unittest
from unittest.mock import patch
from flask import json
from authentication.app import app


class TestAuthenticationAPI(unittest.TestCase):
    def setUp(self):
        """Set up test client."""
        self.app = app.test_client()
        self.app.testing = True

    @patch('authentication.utils.validate_token')
    def test_validate_token_success(self, mock_validate_token):
        """Test validating a token successfully."""
        mock_validate_token.return_value = (1, 'admin')  # Mock valid token

        response = self.app.post('/validate', headers={'Authorization': 'Bearer valid-token'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['user_id'], 1)
        self.assertEqual(data['role'], 'admin')

    @patch('authentication.utils.validate_token')
    def test_validate_token_failure(self, mock_validate_token):
        """Test validating a token that fails."""
        mock_validate_token.return_value = (None, None)  # Mock invalid token

        response = self.app.post('/validate', headers={'Authorization': 'Bearer invalid-token'})
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Invalid token')

    @patch('authentication.utils.validate_token')
    @patch('authentication.utils.is_authorized')
    def test_authorize_success(self, mock_is_authorized, mock_validate_token):
        """Test successful authorization."""
        mock_validate_token.return_value = (1, 'admin')  # Mock valid user
        mock_is_authorized.return_value = True  # Mock valid authorization

        response = self.app.post(
            '/authorize',
            headers={'Authorization': 'Bearer valid-token'},
            json={'resource': 'view_destinations'}
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Authorized')

    @patch('authentication.utils.validate_token')
    @patch('authentication.utils.is_authorized')
    def test_authorize_failure(self, mock_is_authorized, mock_validate_token):
        """Test failed authorization."""
        mock_validate_token.return_value = (1, 'user')  # Mock valid user
        mock_is_authorized.return_value = False  # Mock failed authorization

        response = self.app.post(
            '/authorize',
            headers={'Authorization': 'Bearer valid-token'},
            json={'resource': 'view_destinations'}
        )
        self.assertEqual(response.status_code, 403)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Unauthorized')

    @patch('authentication.utils.validate_token')
    def test_validate_token_missing(self, mock_validate_token):
        """Test validating a request without a token."""
        response = self.app.post('/validate', headers={})  # No token provided
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Token is missing')

    @patch('authentication.utils.validate_token')
    @patch('authentication.utils.is_authorized')
    def test_authorize_invalid_resource(self, mock_is_authorized, mock_validate_token):
        """Test authorization with an invalid resource."""
        mock_validate_token.return_value = (1, 'admin')  # Mock valid user
        mock_is_authorized.return_value = False  # Mock failed authorization

        response = self.app.post(
            '/authorize',
            headers={'Authorization': 'Bearer valid-token'},
            json={'resource': 'invalid_resource'}
        )
        self.assertEqual(response.status_code, 403)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Unauthorized')

    @patch('authentication.utils.validate_token')
    def test_authorize_no_resource(self, mock_validate_token):
        """Test authorization without providing a resource."""
        mock_validate_token.return_value = (1, 'admin')  # Mock valid token

        response = self.app.post(
            '/authorize',
            headers={'Authorization': 'Bearer valid-token'},
            json={}  # No resource provided
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Missing required fields')

    @patch('authentication.utils.validate_token')
    def test_authorize_with_missing_token(self, mock_validate_token):
        """Test authorization without a token."""
        response = self.app.post('/authorize', json={'resource': 'view_destinations'})
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Token is missing')

    @patch('authentication.utils.validate_token')
    def test_authorize_with_invalid_json(self, mock_validate_token):
        """Test authorization with invalid JSON."""
        mock_validate_token.return_value = (1, 'admin')  # Mock valid token
        response = self.app.post(
            '/authorize',
            headers={'Authorization': 'Bearer valid-token'},
            data='invalid json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Invalid JSON format')


if __name__ == '__main__':
    unittest.main()
