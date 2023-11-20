from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}") # path 에 parameter 를 입력할 수 있다.
def read_item(item_id: int):
    return {"item_id": item_id}

