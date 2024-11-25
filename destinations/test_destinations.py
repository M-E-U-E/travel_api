import unittest
from unittest.mock import patch
import json
import requests
import sys
import os

# Add parent directory to path to import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from destinations.app import app, destinations

class TestDestinationsAPI(unittest.TestCase):
    def setUp(self):
        """Set up test client and data"""
        self.app = app.test_client()
        self.app.testing = True
        self.original_destinations = destinations.copy()

    def tearDown(self):
        """Reset data after each test"""
        global destinations
        destinations = self.original_destinations.copy()

    def test_get_destinations(self):
        """Test getting all destinations"""
        response = self.app.get('/destinations')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(isinstance(data, list))
        self.assertTrue(len(data) > 0)

    @patch('requests.post')
    def test_delete_destination_admin(self, mock_post):
        """Test deleting destination as admin"""
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {'role': 'admin'}

        response = self.app.delete('/destinations/1',
            headers={'Authorization': 'Bearer valid-admin-token'}
        )
        self.assertEqual(response.status_code, 200)

    @patch('requests.post')
    def test_delete_destination_unauthorized(self, mock_post):
        """Test deleting destination without admin rights"""
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {'role': 'user'}

        response = self.app.delete('/destinations/1',
            headers={'Authorization': 'Bearer valid-user-token'}
        )
        self.assertEqual(response.status_code, 403)

    def test_delete_destination_no_token(self):
        """Test deleting destination without token"""
        response = self.app.delete('/destinations/1')
        self.assertEqual(response.status_code, 401)

    def test_swagger_access(self):
        """Test swagger documentation access"""
        response = self.app.get('/swagger.json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['info']['title'], 'Destinations API')

def run_tests_with_coverage():
    """Run tests with coverage reporting"""
    import coverage
    
    # Configure coverage
    cov = coverage.Coverage(
        branch=True,
        source=['destinations'],
        omit=[
            '*/site-packages/*',
            '*/tests/*',
            '*/__pycache__/*',
            '*/__init__.py'
        ]
    )
    
    # Start coverage
    cov.start()
    
    # Run tests
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDestinationsAPI)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
    
    # Stop coverage
    cov.stop()
    cov.save()
    
    # Report coverage
    print('\nCoverage Summary:')
    cov.report()
    
    # Generate HTML report
    cov.html_report(directory='coverage_report')

if __name__ == '__main__':
    run_tests_with_coverage() 