from sqlalchemy.orm import Session
from fastapi import HTTPException
from repositories import product_repository
from schemas import product_schema


def create_product(db: Session, request: product_schema.ProductCreate):
    return product_repository.create_product(db, request)


def get_all_products(db: Session):
    products = product_repository.get_all_products(db)
    if not products:
        raise HTTPException(status_code=404, detail="No products found")
    return products


def get_product_by_id(db: Session, product_id: int):
    product = product_repository.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


def search_products(db: Session, name: str = None, category_id: int = None):
    products = product_repository.search_products(db, name, category_id)
    if not products:
        raise HTTPException(status_code=404, detail="No matching products found")
    return products


def delete_product(db: Session, product_id: int):
    product = product_repository.delete_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}
