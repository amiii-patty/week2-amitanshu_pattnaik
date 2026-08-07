from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from db.base import get_db
from schemas import product_schema
from services import product_service
from typing import Optional

router = APIRouter(
    prefix="/api/products",
    tags=["Products"]
)


@router.post("/post", response_model=product_schema.ProductResponse)
def create_product(request: product_schema.ProductCreate, db: Session = Depends(get_db)):
    return product_service.create_product(db, request)


@router.get("", response_model=list[product_schema.ProductResponse])
def list_products(db: Session = Depends(get_db)):
    return product_service.get_all_products(db)

@router.get("/search", response_model=list[product_schema.ProductResponse])
def search_products(
    name: Optional[str] = Query(None),
    category_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    return product_service.search_products(db, name, category_id)


@router.get("/{product_id}", response_model=product_schema.ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    return product_service.get_product_by_id(db, product_id)


@router.delete("/delete/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    return product_service.delete_product(db, product_id)
