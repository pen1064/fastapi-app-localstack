from unittest import TestCase

from fastapi.testclient import TestClient

from app_dynamodb.app import app


class Test(TestCase):
    def setUp(self):
        print("Setting up")
        self.testclient = TestClient(app)

    def teardown(self):
        pass

    def test_root(self):
        url_full = "/"
        response = self.testclient.get(url_full)
        assert response.status_code == 200
        assert response.json() == {"message": "Hello World!"}

    def test_put_item(self):
        url_full_put_dynamo = "/put_dynamodb"
        response_put_dynamo = self.testclient.put(
            url_full_put_dynamo,
            json={
                "author": "CS Lewis",
                "year": 1932,
                "title": "Brave New World",
            },
        )
        self.assertEqual(response_put_dynamo.status_code , 200)
        self.assertEqual(response_put_dynamo.json(), {"message": "Success to place book title Brave New World"})

    def test_get_item(self):
        url_full_get_dynamo = "/get_dynamodb"
        response_get_dynamo = self.testclient.get(
            url_full_get_dynamo,
            json={
                "author": "CS Lewis",
                "year": 1932,
            },
        )
        self.assertEqual(response_get_dynamo.status_code , 200)
        self.assertEqual(response_get_dynamo.json(), {
            "message": "Author CS Lewis has written book title Brave New World in year 1932"
        })
