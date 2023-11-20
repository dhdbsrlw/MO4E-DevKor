from fastapi import FastAPI, HTTPException

app = FastAPI()

# User DB
USER_DB = {}

# Fail Response
NAME_NOT_FOUND - HTTPException(staus_code=400, detail="Name not found.")

# Create
@app.post("/users/name/{name}/nickname/{nickname}")
def create_user(name: str, nickname: str):
    USER_DB[name] = nickname
    return {"status": "success"}

# Read
@app.get("/users/name/{name}")
def read_user(name: str):
    if name not in USER_DB:
        raise NAME_NOT_FOUND
    return {"nickname": USER_DB[name]}

# Update
@app.put("/users/name/{name}/nickname/{nickname}")
def update_user(name:str, nickname: str):
    if name not in USER_DB:
        raise NAME_NOT_FOUND
    USER_DB[name] = nickname
    return {"status": "success"}

# Delete
@app.delete("/users/name/{name}")
def delete_user(name: str):
    if name not in USER_DB:
        raise NAME_NOT_FOUND
    del USER_DB[name]
    return {"status" : "success"}