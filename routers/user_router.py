from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.base import get_db
from schemas import user_schema
from services import user_service
from fastapi.security import OAuth2PasswordRequestForm
from utils.logger import logger

router = APIRouter(
    prefix="/api/users",
    tags=["Users"]
)

@router.post('/register', response_model=user_schema.UserResponse)
def create_user(
    request: user_schema.UserCreate,
    db: Session = Depends(get_db),
):
    logger.info("Register user route started: POST /api/users/register")

    result = user_service.register_user(
        db,
        request,
    )

    logger.info("Register user route completed: POST /api/users/register")
    return result

@router.post("/login", response_model=user_schema.TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    logger.info("Login route started: POST /api/users/login")

    result = user_service.login_user(
        db,
        form_data.username,
        form_data.password,
    )

    logger.info("Login route completed: POST /api/users/login")
    return result


