from sqlalchemy.orm import Session
from schemas import user_schema
from repositories import user_repository
from utils.exceptions import raise_not_found, raise_unauthorized, raise_conflict


def register_user(db: Session, request: user_schema.UserCreate):
    existing = user_repository.get_user_by_email(db, request.email)
    if existing: # Fix: Check for duplicate email before creating a user.
        raise_conflict("An account with this email already exists")
    return user_repository.create_user(db, request)


def login_user(db: Session, request: user_schema.UserLogin):
    user = user_repository.get_user_by_email(db, request.email)

    # Fix: Guard against None BEFORE accessing any attribute on user
    # Previously: user.email on a None object → AttributeError → 500
    
    if not user:                                                   
        raise_not_found("No account found with this email")

    if user.password != request.password:
        raise_unauthorized("Incorrect password")

    return {"message": "Login successful", "user_id": user.user_id, "name": user.name}