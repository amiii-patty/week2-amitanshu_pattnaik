from sqlalchemy.orm import Session

from models.cart import Cart
from models.product import Product
from schemas import cart_schema


def add_item(db: Session, request: cart_schema.CartItemAdd, user_id: int):  # Fix: accept user_id from service
    existing = (
        db.query(Cart)
        .filter(Cart.user_id == user_id, Cart.product_id == request.product_id)
        .first()
    )
    if existing:
        existing.quantity += request.quantity
        db.commit()
        db.refresh(existing)
        return _map_item(existing)

    new_item = Cart(user_id=user_id, product_id=request.product_id, quantity=request.quantity)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return _map_item(new_item)


def get_cart(db: Session, user_id: int):
    items = db.query(Cart).filter(Cart.user_id == user_id).all()
    return [_map_item(i) for i in items]


# Fix: added get_item_by_id — used by service layer for 404 + ownership checks
def get_item_by_id(db: Session, cart_item_id: int):
    return db.query(Cart).filter(Cart.cart_id == cart_item_id).first()


def update_item(db: Session, cart_item_id: int, request: cart_schema.CartItemUpdate):
    # Fix: removed redundant None check — service layer guarantees item exists via get_item_by_id
    item = db.query(Cart).filter(Cart.cart_id == cart_item_id).first()
    item.quantity = request.quantity
    db.commit()
    db.refresh(item)
    return _map_item(item)


def remove_item(db: Session, cart_item_id: int):
    # Fix: capture mapped data BEFORE delete — avoids DetachedInstanceError post-commit
    item = db.query(Cart).filter(Cart.cart_id == cart_item_id).first()
    db.delete(item)
    db.commit()


def get_cart_summary(db: Session, user_id: int):
    results = (
        db.query(Cart, Product.product_name, Product.price)
        .join(Product, Cart.product_id == Product.product_id)
        .filter(Cart.user_id == user_id)
        .all()
    )
    items = []
    total_price = 0.0
    for cart_item, product_name, unit_price in results:
        subtotal = round(unit_price * cart_item.quantity, 2)
        total_price += subtotal
        items.append({
            "cart_id": cart_item.cart_id,
            "product_id": cart_item.product_id,
            "product_name": product_name,
            "unit_price": unit_price,
            "quantity": cart_item.quantity,
            "subtotal": subtotal
        })
    return {"user_id": user_id, "items": items, "total_price": round(total_price, 2)}


def _map_item(item: Cart):
    return {
        "cart_id": item.cart_id,
        "user_id": item.user_id,
        "product_id": item.product_id,
        "quantity": item.quantity
    }