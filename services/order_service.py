
from sqlalchemy.orm import Session
from repositories import order_repository
from schemas import order_schema


def checkout(db: Session, request: order_schema.CheckoutRequest):
    return order_repository.checkout(db, request)

def get_order_history(db: Session, user_id: int):
    return order_repository.get_order_history(db, user_id)

def get_order_details(db: Session, order_id: int):
    return order_repository.get_order_details(db, order_id)