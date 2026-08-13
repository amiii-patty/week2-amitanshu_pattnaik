import pytest

from models.cart import Cart
from models.category import Category
from models.product import Product


def register_and_login(client, username, email):
    response = client.post(
        "/api/users/register",
        json={
            "name": "Test User",
            "username": username,
            "email": email,
            "password": "secret123",
            "mobile": "1234567890",
        },
    )
    assert response.status_code == 200

    user_id = response.json()["user_id"]

    response = client.post(
        "/api/users/login",
        data={
            "username": username,
            "password": "secret123",
        },
    )
    assert response.status_code == 200

    return {
        "user_id": user_id,
        "token": response.json()["access_token"],
    }


def auth_header(user):
    return {"Authorization": f"Bearer {user['token']}"}


def add_to_cart(client, user, product, quantity=2):
    return client.post(
        "/api/cart/",
        json={
            "product_id": product.product_id,
            "quantity": quantity,
        },
        headers=auth_header(user),
    )


def checkout_order(
    client,
    user,
    payment_method="cash",
    user_id=None,
):
    return client.post(
        "/api/orders/",
        json={
            "user_id": user_id or user["user_id"],
            "payment_method": payment_method,
        },
        headers=auth_header(user),
    )


@pytest.fixture()
def customer(client):
    return register_and_login(
        client,
        "customer",
        "customer@example.com",
    )


@pytest.fixture()
def other_customer(client):
    return register_and_login(
        client,
        "othercustomer",
        "other@example.com",
    )


@pytest.fixture()
def product(db_session):
    category = Category(category_name="Electronics")
    db_session.add(category)
    db_session.flush()

    product = Product(
        product_name="Laptop",
        description="Test laptop",
        price=999.99,
        quantity=10,
        url="https://example.com/laptop",
        category_id=category.category_id,
    )

    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    return product


@pytest.fixture()
def completed_order(client, customer, product):
    response = add_to_cart(
        client,
        customer,
        product,
    )
    assert response.status_code == 201

    response = checkout_order(client, customer)
    assert response.status_code == 201

    return response.json()


def test_checkout_creates_order_and_updates_inventory(
    client,
    customer,
    product,
    db_session,
):
    add_response = add_to_cart(
        client,
        customer,
        product,
        quantity=2,
    )
    assert add_response.status_code == 201

    response = checkout_order(client, customer)

    assert response.status_code == 201

    order = response.json()

    assert order["user_id"] == customer["user_id"]
    assert order["payment_method"] == "cash"
    assert order["total_amount"] == pytest.approx(1999.98)

    db_session.expire_all()

    updated_product = (
        db_session.query(Product)
        .filter(Product.product_id == product.product_id)
        .first()
    )

    remaining_cart = (
        db_session.query(Cart)
        .filter(Cart.user_id == customer["user_id"])
        .all()
    )

    assert updated_product.quantity == 8
    assert remaining_cart == []


def test_checkout_uses_logged_in_user(
    client,
    customer,
    product,
):
    add_to_cart(client, customer, product)

    response = checkout_order(
        client,
        customer,
        user_id=9999,
    )

    assert response.status_code == 201
    assert response.json()["user_id"] == customer["user_id"]


def test_checkout_requires_authentication(client):
    response = client.post(
        "/api/orders/",
        json={
            "user_id": 1,
            "payment_method": "cash",
        },
    )

    assert response.status_code == 401


def test_checkout_rejects_empty_cart(client, customer):
    response = checkout_order(client, customer)

    assert response.status_code == 400
    assert response.json()["detail"] == "Cart is empty"


def test_customer_can_view_own_order_history(
    client,
    customer,
    completed_order,
):
    response = client.get(
        f"/api/orders/history/{customer['user_id']}",
        headers=auth_header(customer),
    )

    assert response.status_code == 200

    orders = response.json()

    assert len(orders) == 1
    assert orders[0]["order_id"] == completed_order["order_id"]


def test_customer_cannot_view_another_users_history(
    client,
    customer,
    other_customer,
    product,
):
    add_to_cart(client, other_customer, product)
    checkout_order(client, other_customer)

    response = client.get(
        f"/api/orders/history/{other_customer['user_id']}",
        headers=auth_header(customer),
    )

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "You are not authorized to view this order history"
    )


def test_customer_can_view_order_details(
    client,
    customer,
    completed_order,
):
    order_id = completed_order["order_id"]

    response = client.get(
        f"/api/orders/{order_id}/details",
        headers=auth_header(customer),
    )

    assert response.status_code == 200

    details = response.json()

    assert details["order_id"] == order_id
    assert details["user_id"] == customer["user_id"]
    assert details["items"][0]["product_name"] == "Laptop"