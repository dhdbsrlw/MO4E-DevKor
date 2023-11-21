from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from config.database import create_tables
from routers import user

create_tables()
app = FastAPI()

app.include_router(user.router)

origins = ["*"]

app.add_middleware( # CORS 에러 방지용 (도메인이 다르면 브라우저 단에서 이것을 막으므로 현재는 풀어둔 것이다.)
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}