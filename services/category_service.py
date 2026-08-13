from sqlalchemy.orm import Session

from repositories import category_repository
from schemas import category_schema
from utils.exceptions import raise_conflict, raise_not_found


def create_category(
    db: Session,
    request: category_schema.CategoryCreate,
):
    # Fix: added duplicate name guard before insert
    existing = category_repository.get_category_by_name(
        db,
        request.category_name,
    )

    if existing:
        raise_conflict("Category with this name already exists")

    return category_repository.create_category(db, request)


def get_all_categories(db: Session):
    categories = category_repository.get_all_categories(db)

    # Fix: empty list is a valid state
    return categories


def update_category(
    db: Session,
    category_id: int,
    request: category_schema.CategoryUpdate,
):
    category = category_repository.get_category_by_id(
        db,
        category_id,
    )

    if not category:
        raise_not_found("Category not found")

    existing = category_repository.get_category_by_name(
        db,
        request.category_name,
    )

    # Do not reject the category if it keeps its own current name.
    if existing and existing.category_id != category_id:
        raise_conflict("Category with this name already exists")

    return category_repository.update_category(
        db,
        category_id,
        request,
    )