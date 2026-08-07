from sqlalchemy.orm import Session
from models.category import Category
from schemas import category_schema

def create_category(db: Session, request: category_schema.CategoryCreate):
    new_category = Category(category_name=request.category_name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

def get_all_categories(db: Session):
    return db.query(Category).all()