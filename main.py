from typing import Union

from fastapi import FastAPI , Response
from pydantic import BaseModel
import json
import uuid

app = FastAPI()

f = open('user.json')


class User(BaseModel):
    user_id : str
    email : str
    name : str
    given_name : str
    family_name : str
    nickname : str
    last_ip : str
    logins_count : int
    created_at : str
    updated_at : str
    last_login : str
    email_verified : Union[bool, None] = None

data : list[User] = json.load(f)

@app.get("/")
def read_root():
    return data


@app.get("/user/{user_id}")
def read_item(user_id: str):
    result = (x for x in data if x["user_id"] == user_id)
    return result


@app.put("/items/{user_id}")
def update_item(user_id: str, data_result: User):
    for el in data:
        if el["user_id"] == user_id:
            el.update({
                "email": data_result.email,
                "name": data_result.name,
                "given_name": data_result.given_name,
                "family_name": data_result.family_name,
                "nickname": data_result.nickname,
                "last_ip": data_result.last_ip,
                "logins_count": data_result.logins_count,
                "created_at": data_result.created_at,
                "updated_at": data_result.updated_at,
                "last_login": data_result.last_login,
                "email_verified": data_result.email_verified
            })
    return data

@app.post("/")
def addItem(request:User):
    request.user_id = str(uuid.uuid4())
    data.append(request)
    return data

@app.delete("/del/{user_id}")
def deleteItem(user_id: str):
    index = next((i for i, item in enumerate(data) if item["user_id"] == user_id), -1)
    del data[index]
    return data

f.close()