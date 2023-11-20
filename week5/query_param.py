from fastapi import FastAPI

app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/items/")
def read_item(skip:int = 0, limit:int = 10):
    return fake_items_db[skip:skip+limit]

# Required Query Parameter 
# needy 는 path 에 포함되어 있지 않으므로 Query Parameter 이고, 기본값이 존재하지 않으므로 Required - 이다.
@app.get("/items/{item_id}")
def read_user_item(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}
    return item