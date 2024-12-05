import unittest
import json
from app import app
from tests.test_helpers import get_token


class TestProfile(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_profile_success(self):
        token = get_token(self.app, "admin", "admin123")
        response = self.app.get('/profile', headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['username'], "admin")

    def test_get_profile_unauthorized(self):
        response = self.app.get('/profile', headers={"Authorization": "Bearer invalid_token"})
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Invalid token')


if __name__ == '__main__':
    unittest.main()
