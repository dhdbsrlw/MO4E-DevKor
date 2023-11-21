from pydantic import BaseModel

# 각 스키마 정의
class User(BaseModel):
    id: int
    name: str
    age: int
    role: str
    class Config:
        orm_mode = True
        
class UserUpdate(BaseModel):
    name: str
    age: int
    role: str
    class Config:
        orm_mode = True

class CompleteResponse(BaseModel):
    complete: str
    class Config:
        orm_mode = True
        
        