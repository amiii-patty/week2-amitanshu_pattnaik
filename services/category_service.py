from sqlalchemy.orm import Session
from fastapi import HTTPException
from repositories import category_repository
from schemas import category_schema

def create_category(db: Session, request: category_schema.CategoryCreate):
    return category_repository.create_category(db, request)

def get_all_categories(db: Session):
    categories = category_repository.get_all_categories(db)
    if not categories:
        raise HTTPException(status_code=404, detail="No categories found")
    return categories