from sqlalchemy import Column, DateTime, String, Integer
from sqlalchemy.sql.functions import current_timestamp
from config.database import Base

# User Model - DB 테이블 정보를 입력해주는 역할
class User(Base):
    __tablename__ = "users" # table 이름
    
    user_id = Column( # column 정의
        String(255),
        primary_key=True,
        comment='User ID'
    )
    user_name = Column(
        String(255),
        nullable=False,
        unique=True,
        comment="User Name",
    )
    age = Column(
        Integer,
        nullable=False,
        comment="User Age",
    )
    created_datetime = Column(
        DateTime(timezone=True),
        server_default=current_timestamp(),
        nullable=False,
    )