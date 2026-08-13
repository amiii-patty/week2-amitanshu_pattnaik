def valid_user():
    return {
        "name": "Test User",
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "secret123",
        "mobile": "1234567890",
    }


def register_user(client):
    response = client.post(
        "/api/users/register",
        json=valid_user(),
    )

    assert response.status_code == 200
    return response


def test_register_user(client):
    response = register_user(client)
    user = response.json()

    assert user["name"] == "Test User"
    assert user["username"] == "testuser"
    assert user["email"] == "testuser@example.com"
    assert "user_id" in user
    assert "password" not in user


def test_register_duplicate_email(client):
    register_user(client)

    duplicate_user = valid_user()
    duplicate_user["username"] = "differentuser"

    response = client.post(
        "/api/users/register",
        json=duplicate_user,
    )

    assert response.status_code == 409
    assert response.json()["detail"] == (
        "An account with this email already exists"
    )


def test_register_invalid_email(client):
    invalid_user = valid_user()
    invalid_user["email"] = "not-an-email"

    response = client.post(
        "/api/users/register",
        json=invalid_user,
    )

    assert response.status_code == 422


def test_login_with_valid_credentials(client):
    register_user(client)

    response = client.post(
        "/api/users/login",
        data={
            "username": "testuser",
            "password": "secret123",
        },
    )

    assert response.status_code == 200

    login_data = response.json()

    assert login_data["message"] == "Welcome back, Test User"
    assert login_data["token_type"] == "bearer"
    assert login_data["access_token"]


def test_login_with_wrong_password(client):
    register_user(client)

    response = client.post(
        "/api/users/login",
        data={
            "username": "testuser",
            "password": "wrongpassword",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect password"


def test_login_with_unknown_username(client):
    response = client.post(
        "/api/users/login",
        data={
            "username": "unknownuser",
            "password": "secret123",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == (
        "No account found with this email or username"
    )