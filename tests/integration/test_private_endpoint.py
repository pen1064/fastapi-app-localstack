from unittest import TestCase
from app_dynamodb.helper_functions import create_access_token
from fastapi.testclient import TestClient
import json

from app_dynamodb.app import app


class PrivateEndpointTest(TestCase):
    def setUp(self):
        print("Setting up")
        self.testclient = TestClient(app)
        self.message = {
            "username": "fatcat",
            "full_name": "Fat Cat",
            "email": "info@nekonuts.ca",
            "password": "fatcatisaplushy",
            "active": False,
            }
        self.encoded_token = create_access_token(self.message)

    def teardown(self):
        pass

    def test_home(self):
        url_full = "/home"
        headers = {"Authorization": f"Bearer {self.encoded_token}"}
        response = self.testclient.get(url_full, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Hello fatcat! This is private endpoint"})
