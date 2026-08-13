
from sqlalchemy.orm import Session

from repositories import product_repository, category_repository
from schemas import product_schema
from utils.exceptions import raise_not_found, raise_conflict


def create_product(db: Session, request: product_schema.ProductCreate):
    # Fix: added category existence check to prevent raw IntegrityError on invalid FK
    category = category_repository.get_category_by_id(db, request.category_id)
    if not category:
        raise_not_found("Category not found")

    # Fix: added duplicate product name guard to prevent raw IntegrityError on unique constraint
    existing = product_repository.get_product_by_name(db, request.product_name)
    if existing:
        raise_conflict("Product with this name already exists")

    return product_repository.create_product(db, request)


def get_all_products(db: Session):
    # Fix: empty list is a valid state — return as-is with 200 instead of raising 404
    return product_repository.get_all_products(db)


def get_product_by_id(db: Session, product_id: int):
    product = product_repository.get_product_by_id(db, product_id)
    if not product:
        raise_not_found("Product not found")
    return product


def search_products(db: Session, name: str = None, category_id: int = None):
    # Fix: empty search result is a valid state — return as-is with 200 instead of raising 404
    return product_repository.search_products(db, name, category_id)

def update_product_quantity(
    db: Session,
    product_id: int,
    request: product_schema.ProductUpdateQuantity
):
    product = product_repository.update_product_quantity(db, product_id, request.quantity)
    if not product:
        raise_not_found("Product not found")
    return product


def delete_product(db: Session, product_id: int):
    product = product_repository.delete_product(db, product_id)
    if not product:
        raise_not_found("Product not found")
    return {"message": "Product deleted successfully"}