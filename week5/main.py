# main.py
from fastapi import FastAPI

# Create a FastAPI instance
app = FastAPI()

@app.get("/") # Path Operation Decorator
def read_root():
    return {"Hello": "World"}