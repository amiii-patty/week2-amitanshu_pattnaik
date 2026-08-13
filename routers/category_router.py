from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from db.base import get_db
from schemas import category_schema
from services import category_service
from utils.jwt_handler import require_admin
from utils.logger import logger


router = APIRouter(
    prefix="/api",
    tags=["Categories"],
)


# Fix: added admin path and admin dependency
@router.post(
    "/admin/categories/",
    response_model=category_schema.CategoryResponse,
)
def create_category(
    request: category_schema.CategoryCreate,
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    logger.info(
        "Category route started: POST /api/admin/categories/",
    )

    result = category_service.create_category(
        db,
        request,
    )

    logger.info(
        "Category route completed: POST /api/admin/categories/",
    )

    return result


# Fix: added response_model with List to enforce output schema
@router.get(
    "/categories/list",
    response_model=List[category_schema.CategoryResponse],
)
def list_categories(
    db: Session = Depends(get_db),
):
    logger.info(
        "Category route started: GET /api/categories/list",
    )

    result = category_service.get_all_categories(db)

    logger.info(
        "Category route completed: GET /api/categories/list",
    )

    return result


# Added: admin-only category update endpoint
@router.patch(
    "/admin/categories/{category_id}",
    response_model=category_schema.CategoryResponse,
)
def update_category(
    category_id: int,
    request: category_schema.CategoryUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    logger.info(
        "Category route started: PATCH /api/admin/categories/%s",
        category_id,
    )

    result = category_service.update_category(
        db,
        category_id,
        request,
    )

    logger.info(
        "Category route completed: PATCH /api/admin/categories/%s",
        category_id,
    )

    return result