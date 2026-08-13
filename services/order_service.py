from sqlalchemy.orm import Session

from utils.jwt_handler import TokenData  # Fix: router injects TokenData, not Users
from repositories import order_repository
from schemas import order_schema
from utils.exceptions import raise_not_found, raise_bad_request, raise_forbidden


# Fix: force user_id to logged-in user — prevents placing orders for another user
def checkout(db: Session, request: order_schema.CheckoutRequest, current_user: TokenData):
    # Milestone 1: force user_id from token — client cannot spoof another user's order
    request.user_id = current_user.user_id  # Fix: .id -> .user_id

    try:
        order = order_repository.checkout(db, request)
    except ValueError as e:
        # Fix: catches stock validation error raised in repository and converts to HTTP 400
        raise_bad_request(str(e))

    if not order:
        # Fix: empty cart guard moved to service layer — router no longer needs to check return value
        raise_bad_request("Cart is empty")

    return order


def get_order_history(db: Session, user_id: int, current_user: TokenData):
    # Fix: empty history is a valid state — return [] with 200 instead of raising 404
    if user_id != current_user.user_id:  # Fix: .id -> .user_id
        raise_forbidden("You are not authorized to view this order history")
    return order_repository.get_order_history(db, user_id)


def get_order_details(db: Session, order_id: int, current_user: TokenData):
    order = order_repository.get_order_details(db, order_id)
    if not order:
        raise_not_found("Order not found")

    # Fix: ownership check — prevent user A from viewing user B's order
    if order["user_id"] != current_user.user_id:  # Fix: dict access (repo returns a dict) + .id -> .user_id
        raise_forbidden("You are not authorized to view this order")
    return order

def get_all_orders(db: Session):
    return order_repository.get_all_orders(db)