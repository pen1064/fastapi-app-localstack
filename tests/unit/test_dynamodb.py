from unittest import TestCase

from app_dynamodb.helper_functions import create_dynamodb_table, delete_dynamodb_table, get_dynamodb_client


class DynamodbTest(TestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        self.dynamodb_client = get_dynamodb_client()
        self.table_name = "test-table"
        create_dynamodb_table(self.table_name)

    def teardown(self) -> None:
        print("Tearing down the class")
        delete_dynamodb_table(self.table_name)

    def test_put_item(self):
        response = self.dynamodb_client.put_item(
            TableName=self.table_name,
            Item={"author": {"S": "JK Rowling"}, "year": {"N": "2002"}, "title": {"S": "Harry Potter 1"}},
        )
        self.assertEqual(response.get("ResponseMetadata").get("HTTPStatusCode"), 200)

    def test_get_item(self):
        response = self.dynamodb_client.get_item(
            TableName=self.table_name, Key={"author": {"S": "JK Rowling"}, "year": {"N": "2002"}}
        )
        title = response.get("Item").get("title").get("S")
        self.assertEqual(title, "Harry Potter 1")
