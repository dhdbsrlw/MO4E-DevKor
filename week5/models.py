from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base

# 모델 생성 (테이블 생성)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True) # PK (unique)
    name = Column(String, index=True)
    age = Column(Integer, index=True)
    role = Column(String, index=True)