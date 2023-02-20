from typing import Optional

from pydantic import BaseModel


class DynamodbPutRequest(BaseModel):
    author: str
    year: int
    title: str


class DynamodbGetRequest(BaseModel):
    author: str
    year: Optional[int]


class User(BaseModel):
    username: str
    full_name: str
    email: str
    password: str
    active: bool


