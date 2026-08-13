import pytest

from models.category import Category
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

    admin_user = (
        db_session.query(Users)
        .filter(Users.username == "admin")
        .first()
    )

    admin_user.role = "admin"
    db_session.commit()

    return login_user(client, "admin")


@pytest.fixture()
def category(db_session):
    new_category = Category(category_name="Electronics")
    db_session.add(new_category)
    db_session.commit()
    db_session.refresh(new_category)

    return new_category


def test_list_categories(client, category):
    response = client.get("/api/categories/list")

    assert response.status_code == 200
    assert response.json()[0]["category_name"] == "Electronics"


def test_admin_can_create_category(client, admin_token):
    response = client.post(
        "/api/admin/categories/",
        json={"category_name": "Books"},
        headers=auth_header(admin_token),
    )

    assert response.status_code == 200
    assert response.json()["category_name"] == "Books"


def test_customer_cannot_create_category(client, customer_token):
    response = client.post(
        "/api/admin/categories/",
        json={"category_name": "Books"},
        headers=auth_header(customer_token),
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required"


def test_duplicate_category_is_rejected(
    client,
    admin_token,
    category,
):
    response = client.post(
        "/api/admin/categories/",
        json={"category_name": "Electronics"},
        headers=auth_header(admin_token),
    )

    assert response.status_code == 409
    assert response.json()["detail"] == (
        "Category with this name already exists"
    )


def test_invalid_category_name_is_rejected(
    client,
    admin_token,
):
    response = client.post(
        "/api/admin/categories/",
        json={"category_name": ""},
        headers=auth_header(admin_token),
    )

    assert response.status_code == 422


def test_admin_can_update_category(
    client,
    admin_token,
    category,
):
    response = client.patch(
        f"/api/admin/categories/{category.category_id}",
        json={"category_name": "Updated Electronics"},
        headers=auth_header(admin_token),
    )

    assert response.status_code == 200
    assert response.json()["category_name"] == "Updated Electronics"