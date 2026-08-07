from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.base import get_db
from schemas import user_schema
from services import user_service

router = APIRouter(
    prefix="/api/users",
    tags=["Users"]
)

@router.post('/register')
def create_user(request: user_schema.UserCreate, db: Session = Depends(get_db)):
    return user_service.register_user(db, request)

@router.post("/login")
def login(request: user_schema.UserLogin, db: Session = Depends(get_db)):
    return user_service.login_user(db, request)