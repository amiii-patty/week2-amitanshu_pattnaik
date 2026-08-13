from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from db.base import get_db
from schemas import product_schema
from services import product_service
# Fix: imported get_current_user — used to guard write operations (admin-only routes)
from utils.jwt_handler import require_admin
from utils.logger import logger


router = APIRouter(
    prefix="/api",
    tags=["Products"],
)


# Fix: changed "/post" to "/" — verb does not belong in the path
# Fix: added get_current_user dependency — only authenticated admins can create products
@router.post(
    "/admin/products/",
    response_model=product_schema.ProductResponse,
)
def create_product(
    request: product_schema.ProductCreate,
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    logger.info("Create product route started: POST /api/admin/products/")

    result = product_service.create_product(
        db,
        request,
    )

    logger.info("Create product route completed: POST /api/admin/products/")
    return result


# Fix: changed "" to "/" — empty string route causes 404 in FastAPI
# Public — no auth required, users can browse products without logging in
@router.get(
    "/products/",
    response_model=List[product_schema.ProductResponse],
)
def list_products(
    db: Session = Depends(get_db),
):
    logger.info("List products route started: GET /api/products/")

    result = product_service.get_all_products(db)

    logger.info("List products route completed: GET /api/products/")
    return result


# Public — no auth required, search is part of product discovery flow
@router.get(
    "/products/search",
    response_model=List[product_schema.ProductResponse],
)
def search_products(
    name: Optional[str] = Query(None),
    category_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    logger.info("Search products route started: GET /api/products/search")

    result = product_service.search_products(
        db,
        name,
        category_id,
    )

    logger.info("Search products route completed: GET /api/products/search")
    return result


# Public — no auth required, product detail page is publicly visible
@router.get(
    "/products/{product_id}",
    response_model=product_schema.ProductResponse,
)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    logger.info(
        "Get product route started: GET /api/products/%s",
        product_id,
    )

    result = product_service.get_product_by_id(
        db,
        product_id,
    )

    logger.info(
        "Get product route completed: GET /api/products/%s",
        product_id,
    )

    return result


# Fix: used PATCH instead of PUT — only one field is being updated, not the full resource
# Fix: route is "/{product_id}/quantity" — clearly scoped, no verb in path
# Fix: added get_current_user dependency — only authenticated admins can update stock
@router.patch(
    "/admin/products/{product_id}/quantity",
    response_model=product_schema.ProductResponse,
)
def update_quantity(
    product_id: int,
    request: product_schema.ProductUpdateQuantity,
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    logger.info(
        "Update product quantity route started: "
        "PATCH /api/admin/products/%s/quantity",
        product_id,
    )

    result = product_service.update_product_quantity(
        db,
        product_id,
        request,
    )

    logger.info(
        "Update product quantity route completed: "
        "PATCH /api/admin/products/%s/quantity",
        product_id,
    )

    return result


# Fix: changed "/delete/{product_id}" to "/{product_id}" — verb does not belong in the path
# Fix: added response_model so response is schema-enforced
# Fix: added get_current_user dependency — only authenticated admins can delete products
@router.delete(
    "/admin/products/{product_id}",
    response_model=dict,
)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    logger.info(
        "Delete product route started: DELETE /api/admin/products/%s",
        product_id,
    )

    result = product_service.delete_product(
        db,
        product_id,
    )

    logger.info(
        "Delete product route completed: DELETE /api/admin/products/%s",
        product_id,
    )

    return result