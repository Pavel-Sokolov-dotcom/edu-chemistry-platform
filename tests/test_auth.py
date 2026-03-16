# tests/test_auth.py
from fastapi.testclient import TestClient


def test_register_and_login(client: TestClient):
    """Проверка регистрации и успешного входа"""

    # Регистрация
    register_response = client.post(
        "/api/v1/users/register",
        json={
            "email": "test1@example.com",
            "password": "testpassword",
        },
    )
    assert register_response.status_code in (200, 201)

    # Логин
    login_response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "test1@example.com",
            "password": "testpassword",
        },
    )

    assert login_response.status_code == 200
    data = login_response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client: TestClient):
    """Проверка входа с неверным паролем"""

    # Регистрация
    register_response = client.post(
        "/api/v1/users/register",
        json={
            "email": "test2@example.com",
            "password": "testpassword",
        },
    )
    assert register_response.status_code in (200, 201)

    # Логин с неправильным паролем
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "test2@example.com",
            "password": "wrongpassword",
        },
    )

    assert response.status_code == 401
    data = response.json()
    assert "detail" in data


def test_register_duplicate_email(client: TestClient):
    """Проверка регистрации с существующим email"""

    # Первая регистрация
    response1 = client.post(
        "/api/v1/users/register",
        json={
            "email": "test3@example.com",
            "password": "testpassword",
        },
    )
    assert response1.status_code in (200, 201)

    # Вторая регистрация с тем же email
    response2 = client.post(
        "/api/v1/users/register",
        json={
            "email": "test3@example.com",
            "password": "testpassword",
        },
    )
    assert response2.status_code == 400
    data = response2.json()
    assert "detail" in data
