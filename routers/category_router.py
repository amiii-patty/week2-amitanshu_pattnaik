from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from db.base import get_db
from schemas import category_schema
from services import category_service

router = APIRouter(
    prefix="/api/categories",
    tags=["Categories"]
)

# Fix: changed "/post" to "/" — verb does not belong in the path, POST method is self-describing
# Fix: added response_model to enforce output schema and filter raw SQLAlchemy fields
@router.post("/", response_model=category_schema.CategoryResponse)
def create_category(request: category_schema.CategoryCreate, db: Session = Depends(get_db)):
    return category_service.create_category(db, request)


# Fix: added response_model with List to enforce output schema on list endpoint
@router.get("/list", response_model=List[category_schema.CategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    return category_service.get_all_categories(db)