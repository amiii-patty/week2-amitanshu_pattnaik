import pytest

from models.category import Category
from models.product import Product


def create_user(client, username, email):
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

    user_data = response.json()

    response = client.post(
        "/api/users/login",
        data={
            "username": username,
            "password": "secret123",
        },
    )
    assert response.status_code == 200

    return {
        "user_id": user_data["user_id"],
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

@pytest.fixture()
def customer(client):
    return create_user(
        client,
        "customer",
        "customer@example.com",
    )

@pytest.fixture()
def other_customer(client):
    return create_user(
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


def test_add_item_to_cart(client, customer, product):
    response = add_to_cart(client, customer, product)

    assert response.status_code == 201

    cart_item = response.json()

    assert cart_item["user_id"] == customer["user_id"]
    assert cart_item["product_id"] == product.product_id
    assert cart_item["quantity"] == 2


def test_cart_requires_authentication(client, product):
    response = client.post(
        "/api/cart/",
        json={
            "product_id": product.product_id,
            "quantity": 2,
        },
    )

    assert response.status_code == 401


def test_add_item_with_missing_product(client, customer):
    response = client.post(
        "/api/cart/",
        json={
            "product_id": 9999,
            "quantity": 2,
        },
        headers=auth_header(customer),
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"


def test_invalid_cart_quantity_is_rejected(
    client,
    customer,
    product,
):
    response = add_to_cart(
        client,
        customer,
        product,
        quantity=0,
    )

    assert response.status_code == 422


def test_user_cannot_view_another_users_cart(
    client,
    customer,
    other_customer,
    product,
):
    add_response = add_to_cart(
        client,
        other_customer,
        product,
    )
    assert add_response.status_code == 201

    response = client.get(
        "/api/cart/",
        params={"user_id": other_customer["user_id"]},
        headers=auth_header(customer),
    )

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "You are not authorized to view this cart"
    )


def test_user_can_update_cart_item(client, customer, product):
    add_response = add_to_cart(
        client,
        customer,
        product,
    )
    cart_item_id = add_response.json()["cart_id"]

    response = client.patch(
        f"/api/cart/{cart_item_id}",
        json={"quantity": 5},
        headers=auth_header(customer),
    )

    assert response.status_code == 200
    assert response.json()["quantity"] == 5


def test_user_can_remove_cart_item(client, customer, product):
    add_response = add_to_cart(
        client,
        customer,
        product,
    )
    cart_item_id = add_response.json()["cart_id"]

    response = client.delete(
        f"/api/cart/{cart_item_id}",
        headers=auth_header(customer),
    )

    assert response.status_code == 204