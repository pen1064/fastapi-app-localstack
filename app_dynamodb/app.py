from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app_dynamodb.helper_classes import DynamodbGetRequest, DynamodbPutRequest, User
from app_dynamodb.helper_functions import create_dynamodb_table, get_dynamodb_client, decode_token, create_access_token
from app_dynamodb.users_db import users_db

TABLE_NAME = "test-table"
dynamodb_client = get_dynamodb_client()
create_dynamodb_table("test-table")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

app = FastAPI()

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_info: dict = users_db.get(form_data.username)
    if not user_info:
        raise HTTPException(status_code=400, detail="Incorrect username")
    user = User(**user_info)
    if user.password != form_data.password:
        raise HTTPException(status_code=400, detail="Incorrect password")
    access_token = create_access_token(user_info)
    return {"access_token": access_token, "token_type": "bearer"}



@app.get("/home")
async def private_root(token: str = Depends(oauth2_scheme)):
    print(token)
    user = decode_token(token)
    return {"message": f"Hello {user.get('username')}! This is private endpoint"}

@app.get("/")
async def root():
    return {"message": "Hello World!"}


@app.put("/put_dynamodb")
async def put_dynamodb(request: DynamodbPutRequest):
    author = request.author
    year = str(request.year)
    title = request.title
    try:
        response = dynamodb_client.put_item(
            TableName=TABLE_NAME, Item={"author": {"S": author}, "year": {"N": str(year)}, "title": {"S": title}}
        )
        print(response)
        return {"message": f"Success to place book title {title}"}
    except:
        return {"message": f"Fail to place the book title {title}"}


@app.get("/get_dynamodb")
async def get_dynamodb(request: DynamodbGetRequest):
    author = request.author
    year = request.year

    response = dynamodb_client.get_item(TableName=TABLE_NAME, Key={"author": {"S": author}, "year": {"N": str(year)}})
    print(response)
    title = response.get("Item").get("title").get("S")
    return {"message": f"Author {author} has written book title {title} in year {year}"}
