# main.py
from fastapi import FastAPI

# Create a FastAPI instance
app = FastAPI()

@app.get("/") # Path Operation Decorator
def read_root():
    return {"Hello": "World"}

# uvicorn main:app --reload 명령어 실행 시 해당 .py 파일이 위치한 디렉토리로 이동한 후 실행시켜야 한다.