from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6)
    mobile: str | None = Field(default=None, min_length=10, max_length=10)


class UserResponse(BaseModel):
    user_id: int
    name: str
    username: str
    email: str
    mobile: str | None

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """Shape of the response body returned after successful login."""
    message: str
    access_token: str
    token_type: str = "bearer"