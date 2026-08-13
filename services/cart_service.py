from sqlalchemy.orm import Session

from utils.jwt_handler import TokenData  # Fix: correct type — router injects TokenData, not Users
from repositories import cart_repository, product_repository
from schemas import cart_schema
from utils.exceptions import raise_not_found, raise_bad_request, raise_forbidden


def add_item(db: Session, request: cart_schema.CartItemAdd, current_user: TokenData):
    # Fix: added product existence check to prevent FK IntegrityError on invalid product_id
    product = product_repository.get_product_by_id(db, request.product_id)
    if not product:
        raise_not_found("Product not found")

    # Fix: added stock availability check to prevent adding more than available quantity
    if request.quantity > product["quantity"]:
        raise_bad_request(f"Only {product['quantity']} units available in stock")

    # Fix: pass logged-in user_id to repo (CartItemAdd has no user_id field to mutate)
    return cart_repository.add_item(db, request, current_user.user_id)


def get_cart(db: Session, user_id: int, current_user: TokenData):
    # Fix: empty cart is a valid state — return [] with 200 instead of raising 404
    # Fix: ownership check — prevent user A from reading user B's cart
    if user_id != current_user.user_id:  # Fix: .id -> .user_id
        raise_forbidden("You are not authorized to view this cart")
    return cart_repository.get_cart(db, user_id)


def update_item(db: Session, cart_item_id: int, request: cart_schema.CartItemUpdate, current_user: TokenData):
    # Fix: added 404 guard in service layer — removes need for HTTPException in the router
    item = cart_repository.get_item_by_id(db, cart_item_id)
    if not item:
        raise_not_found("Cart item not found")

    # Fix: ownership check — prevent user A from updating user B's cart item
    if item.user_id != current_user.user_id:  # Fix: .id -> .user_id
        raise_forbidden("You are not authorized to update this cart item")
    return cart_repository.update_item(db, cart_item_id, request)


def remove_item(db: Session, cart_item_id: int, current_user: TokenData):
    # Fix: added 404 guard in service layer — removes need for HTTPException in the router
    item = cart_repository.get_item_by_id(db, cart_item_id)
    if not item:
        raise_not_found("Cart item not found")

    # Fix: ownership check — prevent user A from deleting user B's cart item
    if item.user_id != current_user.user_id:  # Fix: .id -> .user_id
        raise_forbidden("You are not authorized to remove this cart item")
    cart_repository.remove_item(db, cart_item_id)


def get_cart_summary(db: Session, user_id: int, current_user: TokenData):
    # Fix: ownership check — prevent user A from reading user B's cart summary
    if user_id != current_user.user_id:  # Fix: .id -> .user_id
        raise_forbidden("You are not authorized to view this cart summary")
    return cart_repository.get_cart_summary(db, user_id)