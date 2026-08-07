from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.base import get_db
from schemas import category_schema
from services import category_service

router = APIRouter(
    prefix="/api/categories",
    tags=["Categories"]
)

@router.post("/post")
def create_category(request: category_schema.CategoryCreate, db: Session = Depends(get_db)):
    return category_service.create_category(db, request)

@router.get("/list")
def list_categories(db: Session = Depends(get_db)):
    return category_service.get_all_categories(db)
