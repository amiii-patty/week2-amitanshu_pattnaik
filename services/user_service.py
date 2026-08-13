from sqlalchemy.orm import Session
from schemas import user_schema
from repositories import user_repository
from utils.exceptions import raise_not_found, raise_unauthorized, raise_conflict
from utils.hashing import hash_password, verify_password
from utils.jwt_handler import create_access_token


def register_user(db: Session, request: user_schema.UserCreate):
    if user_repository.get_user_by_email(db, request.email):
        raise_conflict("An account with this email already exists")

    if user_repository.get_user_by_username(db, request.username):
        raise_conflict("This username is already taken")

    hashed = hash_password(request.password)
    return user_repository.create_user(db, request, hashed)


def login_user(db: Session, identifier: str, password: str):  # ← only line that changed
    db_user = (
        user_repository.get_user_by_email(db, identifier)
        if "@" in identifier
        else user_repository.get_user_by_username(db, identifier)
    )


    # Fix: Guard against None BEFORE accessing any attribute on user
    # Previously: user.email on a None object → AttributeError → 500
    
    if not db_user:
        raise_not_found("No account found with this email or username")

    if not verify_password(password, db_user.password):  
        raise_unauthorized("Incorrect password")

    token = create_access_token({"user_id": db_user.user_id, "role": db_user.role})
    return {
        "message": f"Welcome back, {db_user.name}",
        "access_token": token,
        "token_type": "bearer",
    }