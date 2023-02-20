import boto3
import botocore
from datetime import datetime, timezone, timedelta
from jwt import JWT, jwk_from_pem
from jwt.utils import get_int_from_datetime


CONFIG = botocore.config.Config(retries={"max_attempts": 2})
instance = JWT()

def get_dynamodb_client():
    return boto3.client(
        "dynamodb",
        aws_access_key_id="test",
        aws_secret_access_key="test",
        region_name="us-east-1",
        endpoint_url="http://localhost:4566",
        config=CONFIG,
    )


def create_dynamodb_table(table_name: str):
    dynamodb_client = get_dynamodb_client()
    existing_tables = dynamodb_client.list_tables()["TableNames"]
    if table_name not in existing_tables:
        dynamodb_table = dynamodb_client.create_table(
            TableName=table_name,
            AttributeDefinitions=[
                {"AttributeName": "year", "AttributeType": "N"},
                {"AttributeName": "author", "AttributeType": "S"},
            ],
            KeySchema=[
                {
                    "AttributeName": "author",
                    "KeyType": "HASH",
                },
                {"AttributeName": "year", "KeyType": "RANGE"},
            ],
            ProvisionedThroughput={
                "ReadCapacityUnits": 1,
                "WriteCapacityUnits": 1,
            },
        )
    else:
        pass


def delete_dynamodb_table(table_name: str):
    dynamodb_client = get_dynamodb_client()
    dynamodb_client.delete_table(TableName=table_name)

def create_access_token(data: dict):
    message = data.copy()
    expiration_time_epoch = get_int_from_datetime(datetime.now(timezone.utc) + timedelta(hours=2))
    message.update({'expiration_time': expiration_time_epoch})
    with open('.private/jwtRSA256-private.pem', 'rb') as fh:
        signing_key = jwk_from_pem(fh.read())
    encoded_token = instance.encode(message, signing_key, alg='RS256')
    return encoded_token

def decode_token(token: str):
    with open('jwtRSA256-public.pem', 'rb') as fh:
        verifying_key = jwk_from_pem(fh.read())

    decoded_token = instance.decode(token, verifying_key, do_time_check=True)
    return decoded_token