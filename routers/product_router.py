from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from db.base import get_db
from schemas import product_schema
from services import product_service

router = APIRouter(
    prefix="/api/products",
    tags=["Products"]
)


# Fix: changed "/post" to "/" — verb does not belong in the path
@router.post("/", response_model=product_schema.ProductResponse)
def create_product(request: product_schema.ProductCreate, db: Session = Depends(get_db)):
    return product_service.create_product(db, request)


# Fix: changed "" to "/" — empty string route causes 404 in FastAPI
@router.get("/", response_model=List[product_schema.ProductResponse])
def list_products(db: Session = Depends(get_db)):
    return product_service.get_all_products(db)


@router.get("/search", response_model=List[product_schema.ProductResponse])
def search_products(
    name: Optional[str] = Query(None),
    category_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    return product_service.search_products(db, name, category_id)


@router.get("/{product_id}", response_model=product_schema.ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    return product_service.get_product_by_id(db, product_id)

# Fix: used PATCH instead of PUT — only one field is being updated, not the full resource
# Fix: route is "/{product_id}/quantity" — clearly scoped, no verb in path
@router.patch("/{product_id}/quantity", response_model=product_schema.ProductResponse)
def update_quantity(
    product_id: int,
    request: product_schema.ProductUpdateQuantity,
    db: Session = Depends(get_db)
):
    return product_service.update_product_quantity(db, product_id, request)

# Fix: changed "/delete/{product_id}" to "/{product_id}" — verb does not belong in the path
# Fix: added response_model so response is schema-enforced
@router.delete("/{product_id}", response_model=dict)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    return product_service.delete_product(db, product_id)