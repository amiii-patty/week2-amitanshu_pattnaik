from sqlalchemy.orm import Session
from repositories import cart_repository
from schemas import cart_schema


def add_item(db: Session, request: cart_schema.CartItemAdd):
    return cart_repository.add_item(db, request)

def get_cart(db: Session, user_id: int):
    return cart_repository.get_cart(db, user_id)

def update_item(db: Session, cart_item_id: int, request: cart_schema.CartItemUpdate):
    return cart_repository.update_item(db, cart_item_id, request)

def remove_item(db: Session, cart_item_id: int):
    return cart_repository.remove_item(db, cart_item_id)

def get_cart_summary(db: Session, user_id: int):
    return cart_repository.get_cart_summary(db, user_id)