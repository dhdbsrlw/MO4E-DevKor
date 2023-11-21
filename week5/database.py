# ref: https://backendcode.tistory.com/225

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# postgreSQL 사용하여 DB connection
SQLALCHEMY_DATABASE_URL = "postgresql://yoonjinoh:{password}@localhost:5432/DevKor_user" # git 공개용으로 pasword 는 비공개 처리

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()