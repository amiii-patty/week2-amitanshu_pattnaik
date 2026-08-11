from sqlalchemy.orm import Session

from repositories import order_repository
from schemas import order_schema
from utils.exceptions import raise_not_found, raise_bad_request


def checkout(db: Session, request: order_schema.CheckoutRequest):
    try:
        order = order_repository.checkout(db, request)
    except ValueError as e:
        # Fix: catches stock validation error raised in repository and converts to HTTP 400
        raise_bad_request(str(e))

    if not order:
        # Fix: empty cart guard moved to service layer — router no longer needs to check return value
        raise_bad_request("Cart is empty")

    return order


def get_order_history(db: Session, user_id: int):
    # Fix: empty history is a valid state — return [] with 200 instead of raising 404
    return order_repository.get_order_history(db, user_id)


def get_order_details(db: Session, order_id: int):
    order = order_repository.get_order_details(db, order_id)
    if not order:
        raise_not_found("Order not found")
    return order