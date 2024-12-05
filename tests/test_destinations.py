import unittest
from unittest.mock import patch
import json
import sys
import os

# Add parent directory to path to import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from destinations.app import app, destinations  # Import app and destinations data

class TestDestinationsAPI(unittest.TestCase):
    def setUp(self):
        """Set up test client and mock data."""
        self.app = app.test_client()
        self.app.testing = True
        self.original_destinations = destinations.copy()
        destinations.clear()
        # Add mock destinations
        destinations.extend([
            {'id': 1, 'name': 'Paris', 'location': 'France'},
            {'id': 2, 'name': 'New York', 'location': 'USA'}
        ])

    def tearDown(self):
        """Reset destinations data after each test."""
        global destinations
        destinations = self.original_destinations.copy()

    def test_get_destinations(self):
        """Test getting the list of destinations."""
        response = self.app.get('/destinations')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

    @patch('requests.post')
    def test_delete_destination_admin(self, mock_post):
        """Test deleting a destination with admin role."""
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {'role': 'admin'}

        response = self.app.delete(
            '/destinations/1',
            headers={'Authorization': 'Bearer valid-admin-token'}
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Destination 1 deleted successfully')

    @patch('requests.post')
    def test_delete_destination_nonexistent(self, mock_post):
        """Test deleting a destination that doesn't exist."""
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {'role': 'admin'}

        response = self.app.delete(
            '/destinations/999',
            headers={'Authorization': 'Bearer valid-admin-token'}
        )
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Destination not found')

    @patch('requests.post')
    def test_delete_destination_unauthorized(self, mock_post):
        """Test deleting a destination with non-admin role."""
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {'role': 'user'}

        response = self.app.delete(
            '/destinations/1',
            headers={'Authorization': 'Bearer valid-user-token'}
        )
        self.assertEqual(response.status_code, 403)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Admin access required')

    def test_delete_destination_no_token(self):
        """Test deleting a destination without a token."""
        response = self.app.delete('/destinations/1')
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Token is missing')

    def test_add_destination(self):
        """Test adding a new destination."""
        new_destination = {
            'name': 'Tokyo',
            'description': 'The capital of Japan',
            'location': 'Japan',
            'price_per_night': 200.0
        }
        response = self.app.post('/destinations', json=new_destination)
        self.assertEqual(response.status_code, 201)
        added_destination = json.loads(response.data)
        self.assertEqual(added_destination['name'], new_destination['name'])
        self.assertEqual(len(destinations), 3)  # Assuming there were initially 2 destinations

    def test_add_destination_invalid_data(self):
        """Test adding a destination with missing fields."""
        new_destination = {'name': 'Tokyo'}  # Missing description, location, and price_per_night
        response = self.app.post('/destinations', json=new_destination)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Missing required fields')

    def test_delete_invalid_id(self):
        """Test deleting a destination with an invalid ID format."""
        response = self.app.delete('/destinations/abc', headers={'Authorization': 'Bearer valid-admin-token'})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Invalid destination ID format')

    def test_swagger_spec(self):
        """Test fetching the Swagger specification."""
        response = self.app.get('/swagger.json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['info']['title'], 'Destinations API')

if __name__ == '__main__':
    unittest.main()
