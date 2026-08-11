from sqlalchemy.orm import Session

from models.category import Category
from schemas import category_schema


def create_category(db: Session, request: category_schema.CategoryCreate):
    new_category = Category(category_name=request.category_name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


# Fix: added get_category_by_name to support the duplicate check in the service layer
def get_category_by_name(db: Session, category_name: str):
    return db.query(Category).filter(Category.category_name == category_name).first()

# Fix: added get_category_by_id to support category existence check in product_service
def get_category_by_id(db: Session, category_id: int):
    return db.query(Category).filter(Category.category_id == category_id).first()

def get_all_categories(db: Session):
    return db.query(Category).all()