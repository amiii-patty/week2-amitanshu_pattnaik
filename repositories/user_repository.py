from sqlalchemy.orm import Session
from models import user
from schemas import user_schema

def create_user(db: Session, request: user_schema.UserCreate):
    new_user = user.Users(
        name=request.name,
        email=request.email,
        password=request.password,
        mobile=request.mobile
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_by_email(db:Session, email: str):
    return db.query(user.Users).filter(user.Users.email == email).first()