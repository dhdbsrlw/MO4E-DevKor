# Request Body 는 client 에서 API 로 전송하는 데이터를 의미한다.
# Response Body 는 API 가 client 로 전송하는 데이터를 의미한다.
# client 와 API 간 데이터를 주고 받을 때, 데이터의 형식을 지정해줄 수 있는데 이를 위해 Pydantic Model 을 사용할 수 있다.

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

USER_DB = {}

# FAIL response
NAME_NOT_FOUND = HTTPException(status_code=400, detail="Name not found.")

# Define Input Schema
class CreateIn(BaseModel):
    name: str
    nickname: str
    
# Define Output Schema
class CreateOut(BaseModel):
    status: str
    id: int
    
# Create  
@app.post("/users", response_model=CreateOut)
def create_user(user: CreateIn) -> CreateOut:
    USER_DB[user.name] = user.nickname
    user_dict = user.model_dump() # user.dict() 대체재
    user_dict["status"] = "success"
    user_dict["id"] = len(USER_DB)
    return user_dict

@app.get("/users")
def read_user(name: str):
    if name not in USER_DB:
        raise NAME_NOT_FOUND
    return {"nickname" : USER_DB[name]}

@app.put("/users")
def update_user(name: str, nickname: str):
    if name not in USER_DB:
        raise NAME_NOT_FOUND
    USER_DB[name] = nickname
    return {"status": "success"}

@app.delete("/users")
def delete_user(name: str):
    if name not in USER_DB:
        raise NAME_NOT_FOUND
    del USER_DB[name]
    return {"status": "success"}
         

# Pydantic Model 을 사용하면, 입력받는 파라미터와 생성 후 반환하는 파라미터를 다르게 지정해 줄 수 있다.
    