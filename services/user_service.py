from sqlalchemy.orm import Session
from schemas import user_schema
from fastapi import HTTPException
from repositories import user_repository

def register_user(db: Session, request: user_schema.UserCreate):
    return user_repository.create_user(db, request)

def login_user(db: Session, request: user_schema.UserLogin):
    user = user_repository.get_user_by_email(db, request.email)

    if user.email == request.email and user.password == request.password:
        return {"message": "Login successful", "user_id": user.user_id, "name": user.name}
    else:
        raise HTTPException(status_code=401, detail="Invalid email or password")