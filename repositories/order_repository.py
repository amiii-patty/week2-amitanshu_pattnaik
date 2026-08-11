from sqlalchemy.orm import Session

from models.order import Order
from models.orderDetails import OrderDetails
from models.cart import Cart
from models.product import Product
from schemas import order_schema


def checkout(db: Session, request: order_schema.CheckoutRequest):
    cart_items = (
        db.query(Cart, Product)
        # Fix: changed Product.price to full Product join — needed to update quantity on the same object
        .join(Product, Cart.product_id == Product.product_id)
        .filter(Cart.user_id == request.user_id)
        .all()
    )

    if not cart_items:
        return None

    # Fix: added stock validation — raises if any item exceeds available stock before any DB write
    for cart_item, product in cart_items:
        if cart_item.quantity > product.quantity:
            raise ValueError(
                f"Insufficient stock for '{product.product_name}': "
                f"requested {cart_item.quantity}, available {product.quantity}"
            )

    total_amount = round(sum(cart_item.quantity * product.price for cart_item, product in cart_items), 2)

    new_order = Order(
        user_id=request.user_id,
        payment_method=request.payment_method,
        total_amount=total_amount
    )
    db.add(new_order)
    db.flush()  # get order_id before committing

    for cart_item, product in cart_items:
        detail = OrderDetails(
            order_id=new_order.order_id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            price=product.price
        )
        db.add(detail)

        # Fix: deduct ordered quantity from the product table at time of checkout
        product.quantity -= cart_item.quantity

    # Clear cart after checkout
    db.query(Cart).filter(Cart.user_id == request.user_id).delete()

    db.commit()
    db.refresh(new_order)
    return _map_order(new_order)


def get_order_history(db: Session, user_id: int):
    orders = db.query(Order).filter(Order.user_id == user_id).all()
    return [_map_order(o) for o in orders]


def get_order_details(db: Session, order_id: int):
    order = db.query(Order).filter(Order.order_id == order_id).first()
    if not order:
        return None

    results = (
        db.query(OrderDetails, Product.product_name)
        .join(Product, OrderDetails.product_id == Product.product_id)
        .filter(OrderDetails.order_id == order_id)
        .all()
    )

    items = [
        {
            "details_id": detail.details_id,
            "product_id": detail.product_id,
            "product_name": product_name,
            "quantity": detail.quantity,
            "price": detail.price,
            # Fix: rounded subtotal to avoid floating point drift
            "subtotal": round(detail.price * detail.quantity, 2)
        }
        for detail, product_name in results
    ]

    return {
        "order_id": order.order_id,
        "user_id": order.user_id,
        "order_date": order.order_date,
        "payment_method": order.payment_method,
        "total_amount": order.total_amount,
        "items": items
    }


def _map_order(order: Order):
    return {
        "order_id": order.order_id,
        "user_id": order.user_id,
        "order_date": order.order_date,
        "payment_method": order.payment_method,
        "total_amount": order.total_amount
    }