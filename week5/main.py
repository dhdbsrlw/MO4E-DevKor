# DevKor 회원관리 시스템
# DB 연결 ref) https://do-hyeon.tistory.com/286

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal, engine
import crud
import models
import schemas

# DB 및 TABLE 생성
models.Base.metadata.create_all(bind=engine) # 오류 시 수정 필요

app = FastAPI()

# ---------------------------------------------------------------------------

# USER_DB = {}
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

USER_NOT_FOUND = HTTPException(status_code=400, detail="User not found.") # FAIL

# -----------------------------------------------------------------------------
# (REST API 명세) 수정 필요
# ENDPOINTS

# 특정 추가
@app.post("/users", response_model=schemas.User)
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    db_user = crud.create_user(db=db, user=user)
    return db_user

# 전체 조회
@app.get("/users", response_model=list[schemas.User])
def read_users(skip: int=0, limit: int=100, db: Session=Depends(get_db)):
    users = crud.get_users(db=db, skip=skip, limit=limit)
    return users

# 특정 조회
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session=Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise USER_NOT_FOUND
    return db_user
    
# 특정 수정 (id 는 수정 불가)
@app.put("/users/{user_id}", response_model=schemas.CompleteResponse)
def update_user(user_id: int, user_data: schemas.UserUpdate, db: Session=Depends(get_db)): # 수정 필요
    # 체크
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise USER_NOT_FOUND
    action = crud.update_user(db=db, user_id=user_id, name=user_data.name, age=user_data.age, role=user_data.role)
    return action
    
# 특정 삭제
@app.delete("/users/{user_id}", response_model=schemas.CompleteResponse)
def delete_user(user_id: int, db: Session=Depends(get_db)):
    # 체크
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise USER_NOT_FOUND
    action = crud.delete_user(db=db, user_id=user_id)
    return action
    