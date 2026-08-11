
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6)
    mobile: str | None = Field(default=None, min_length=10, max_length=10)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    user_id: int          
    name: str
    email: str
    mobile: str | None    

    class Config:
        from_attributes = True