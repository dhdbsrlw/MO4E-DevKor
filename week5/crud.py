from sqlalchemy.orm import Session

import models
import schemas


def create_user(db: Session, user: schemas.User):
    db_user = models.User(id=user.id, name=user.name, age=user.age, role=user.role) 
    db.add(db_user)
    # save the changes to DB
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# skip: 처음 N 개의 레코드는 건너뛰고 값을 반환
# limit: 최대 반환하는 레코드의 수 제한
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def update_user(db: Session, user_id: int, name: str, age: int, role: str):
    user_info = db.query(models.User).filter(models.User.id == user_id).first()
    # update
    user_info.name = name
    user_info.age = age
    user_info.role = role
    # save the changes to DB
    db.commit()
    return {"status" : "success"}

def delete_user(db: Session, user_id: int):
    user_info = db.query(models.User).filter(models.User.id == user_id).first()
    # delete in DB (not local)
    db.delete(user_info)
    # save the changes to DB
    db.commit()
    return {"status" : "success"}