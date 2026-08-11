from sqlalchemy.orm import Session

from repositories import cart_repository, product_repository
from schemas import cart_schema
from utils.exceptions import raise_not_found


def add_item(db: Session, request: cart_schema.CartItemAdd):
    # Fix: added product existence check to prevent FK IntegrityError on invalid product_id
    product = product_repository.get_product_by_id(db, request.product_id)
    if not product:
        raise_not_found("Product not found")

    # Fix: added stock availability check to prevent adding more than available quantity
    if request.quantity > product.quantity:
        from utils.exceptions import raise_bad_request
        raise_bad_request(f"Only {product.quantity} units available in stock")

    return cart_repository.add_item(db, request)


def get_cart(db: Session, user_id: int):
    # Fix: empty cart is a valid state — return [] with 200 instead of raising 404
    return cart_repository.get_cart(db, user_id)


def update_item(db: Session, cart_item_id: int, request: cart_schema.CartItemUpdate):
    # Fix: added 404 guard in service layer — removes need for HTTPException in the router
    item = cart_repository.update_item(db, cart_item_id, request)
    if not item:
        raise_not_found("Cart item not found")
    return item


def remove_item(db: Session, cart_item_id: int):
    # Fix: added 404 guard in service layer — removes need for HTTPException in the router
    item = cart_repository.remove_item(db, cart_item_id)
    if not item:
        raise_not_found("Cart item not found")


def get_cart_summary(db: Session, user_id: int):
    return cart_repository.get_cart_summary(db, user_id)

