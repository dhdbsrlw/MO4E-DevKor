import datetime
from pydantic import BaseModel
from typing import List, Optional


class UserBase(BaseModel): # User 라는 모델에 꼭 기본적으로 들어가야 하는 내용
    user_name: str
    age: int

class UserCreate(UserBase):
    pass # UserBase 상속받는다. (사용자로부터 입력받는 정보)

class User(UserBase): # 실제 User 정보는 상속 + 서버에서 자동적으로 생성되는 것까지 포함되어야 한다. 
    user_id: str
    created_datetime: datetime.datetime
    
    class Config:
        orm_mode = True

class UserAll(BaseModel): # 모든 User 를 불러오고 싶은 경우
    total: int
    users: Optional[List[User]]