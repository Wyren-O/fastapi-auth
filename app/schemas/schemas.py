from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
class UserUpdate(BaseModel):
    email: Optional[EmailStr]
    password: Optional[str]
    
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    
    class Config:
        from_attributes = True
