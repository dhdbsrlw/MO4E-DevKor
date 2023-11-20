from fastapi import FastAPI, HTTPException

app = FastApi()

# User DB
USER_DB = {}

# Fail Response
NAME_NOT_FOUND - HTTPException(staus_code=400, detail="Name not found.")


# Create
@app.post("/users")
def create_user(name: str, nickname: str):
    USER_DB[name] = nickname
    return {"status": "success"}


# Read
@app.get("/users")
def read_user(name: str):
    if name not in USER_DB:
        raise NAME_NOT_FOUND
    return {"nickname" : USER_DB[name]}

# Update
@app.put("/users")
def update_user(name: str, nickname: str):
    if name not in USER_DB:
        raise NAME_NO_FOUND
    USER_DB[name] = nickname
    return {"status": "success"}

# Delete
@app.delete("/users")
def delete_user(name: str):
    if name not in USER_DB:
        raise NAME_NOT_FOUND
    del USER_DB[name]
    return {"status": "success"}

