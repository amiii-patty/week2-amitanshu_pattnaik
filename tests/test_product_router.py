import pytest

from models.category import Category
from models.product import Product
from models.user import Users


def register_user(client, username, email):
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


def login_user(client, username):
    response = client.post(
        "/api/users/login",
        data={
            "username": username,
            "password": "secret123",
        },
    )
    assert response.status_code == 200
    return response.json()["access_token"]


def auth_header(token):
    return {"Authorization": f"Bearer {token}"}


def product_data(category_id, product_name="Laptop"):
    return {
        "product_name": product_name,
        "description": "A useful test product",
        "price": 999.99,
        "quantity": 10,
        "url": "https://example.com/laptop",
        "category_id": category_id,
    }


def create_product(db_session, category_id, name="Laptop"):
    product = Product(
        product_name=name,
        description="A useful test product",
        price=999.99,
        quantity=10,
        url="https://example.com/laptop",
        category_id=category_id,
    )
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)
    return product


@pytest.fixture()
def category(db_session):
    category = Category(category_name="Electronics")
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)
    return category


@pytest.fixture()
def product(db_session, category):
    return create_product(
        db_session,
        category.category_id,
    )


@pytest.fixture()
def customer_token(client):
    register_user(
        client,
        "customer",
        "customer@example.com",
    )
    return login_user(client, "customer")


@pytest.fixture()
def admin_token(client, db_session):
    register_user(
        client,
        "admin",
        "admin@example.com",
    )

    admin = (
        db_session.query(Users)
        .filter(Users.username == "admin")
        .first()
    )
    admin.role = "admin"
    db_session.commit()

    return login_user(client, "admin")


def test_public_products_and_search(
    client,
    db_session,
    category,
):
    create_product(db_session, category.category_id, "Laptop")
    create_product(db_session, category.category_id, "Phone")

    list_response = client.get("/api/products/")

    assert list_response.status_code == 200
    assert len(list_response.json()) == 2

    search_response = client.get(
        "/api/products/search",
        params={"name": "Laptop"},
    )

    assert search_response.status_code == 200
    assert len(search_response.json()) == 1
    assert search_response.json()[0]["product_name"] == "Laptop"


def test_product_details_and_missing_product(
    client,
    product,
):
    response = client.get(
        f"/api/products/{product.product_id}",
    )

    assert response.status_code == 200
    assert response.json()["product_name"] == "Laptop"
    assert response.json()["category_name"] == "Electronics"

    missing_response = client.get("/api/products/9999")

    assert missing_response.status_code == 404
    assert missing_response.json()["detail"] == "Product not found"


def test_admin_can_create_product(
    client,
    category,
    admin_token,
):
    response = client.post(
        "/api/admin/products/",
        json=product_data(category.category_id),
        headers=auth_header(admin_token),
    )

    assert response.status_code == 200
    assert response.json()["product_name"] == "Laptop"
    assert response.json()["quantity"] == 10


def test_customer_cannot_create_product(
    client,
    category,
    customer_token,
):
    response = client.post(
        "/api/admin/products/",
        json=product_data(category.category_id),
        headers=auth_header(customer_token),
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required"


def test_admin_can_update_product_quantity(
    client,
    product,
    admin_token,
):
    response = client.patch(
        f"/api/admin/products/{product.product_id}/quantity",
        json={"quantity": 25},
        headers=auth_header(admin_token),
    )

    assert response.status_code == 200
    assert response.json()["quantity"] == 25


def test_admin_can_delete_product(
    client,
    product,
    admin_token,
):
    response = client.delete(
        f"/api/admin/products/{product.product_id}",
        headers=auth_header(admin_token),
    )

    assert response.status_code == 200
    assert response.json()["message"] == (
        "Product deleted successfully"
    )