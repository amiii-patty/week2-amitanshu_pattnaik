from sqlalchemy.orm import Session

from models.cart import Cart
from models.product import Product
from schemas import cart_schema


def add_item(db: Session, request: cart_schema.CartItemAdd):
    existing = (
        db.query(Cart)
        .filter(Cart.user_id == request.user_id, Cart.product_id == request.product_id)
        .first()
    )
    if existing:
        existing.quantity += request.quantity
        db.commit()
        db.refresh(existing)
        return _map_item(existing)

    new_item = Cart(
        user_id=request.user_id,
        product_id=request.product_id,
        quantity=request.quantity
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return _map_item(new_item)


def get_cart(db: Session, user_id: int):
    items = db.query(Cart).filter(Cart.user_id == user_id).all()
    return [_map_item(i) for i in items]


def update_item(db: Session, cart_item_id: int, request: cart_schema.CartItemUpdate):
    item = db.query(Cart).filter(Cart.cart_id == cart_item_id).first()
    if not item:
        return None
    item.quantity = request.quantity
    db.commit()
    db.refresh(item)
    return _map_item(item)


def remove_item(db: Session, cart_item_id: int):
    item = db.query(Cart).filter(Cart.cart_id == cart_item_id).first()
    if item:
        db.delete(item)
        db.commit()
    return item


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
        subtotal = round(unit_price * cart_item.quantity, 2)  # Fix: rounded subtotal to avoid errors
        total_price += subtotal
        items.append({
            "cart_id": cart_item.cart_id,
            "product_id": cart_item.product_id,
            "product_name": product_name,
            "unit_price": unit_price,
            "quantity": cart_item.quantity,
            "subtotal": subtotal
        })
    # Fix: rounded total_price to avoid errors
    return {"user_id": user_id, "items": items, "total_price": round(total_price, 2)}


def _map_item(item: Cart):
    return {
        "cart_id": item.cart_id,
        "user_id": item.user_id,
        "product_id": item.product_id,
        "quantity": item.quantity
    }