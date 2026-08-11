from sqlalchemy.orm import Session

from repositories import category_repository
from schemas import category_schema
from utils.exceptions import raise_conflict  # Fix: removed HTTPException import — HTTP concerns moved out of service layer


def create_category(db: Session, request: category_schema.CategoryCreate):
    # Fix: added duplicate name guard before insert to prevent raw IntegrityError crash
    existing = category_repository.get_category_by_name(db, request.category_name)
    if existing:
        raise_conflict("Category with this name already exists")
    return category_repository.create_category(db, request)


def get_all_categories(db: Session):
    categories = category_repository.get_all_categories(db)
    # Fix: empty list is a valid state, return it as it is with 200 instead of raising 404
    return categories