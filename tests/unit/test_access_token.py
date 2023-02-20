from unittest import TestCase
from app_dynamodb.helper_functions import create_access_token, decode_token

class AccessTokenTest(TestCase):
    def setUp(self) -> None:
        self.message = {
            "username": "fatcat",
            "full_name": "Fat Cat",
            "email": "info@nekonuts.ca",
            "password": "fatcatisaplushy",
            "active": False,
            }

    def tearDown(self) -> None:
        pass

    def test_encode_decode_token(self):
        encoded_token = create_access_token(self.message)
        decode_message = decode_token(encoded_token)
        self.assertEqual(decode_message.get('username'), self.message.get('username'))
        self.assertEqual(decode_message.get('email'), self.message.get('email'))
        self.assertEqual(decode_message.get('password'), self.message.get('password'))
        self.assertEqual(decode_message.get('active'), self.message.get('active'))
        self.assertEqual(decode_message.get('full_name'), self.message.get('full_name'))
