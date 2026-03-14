import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_and_login(client: AsyncClient):
    """Проверка регистрации и успешного входа"""
    
    # Регистрация
    register_response = await client.post(
        "/api/v1/users/register",
        json={
            "email": "test1@example.com",
            "password": "testpassword",
        },
    )
    assert register_response.status_code in (200, 201)
    
    # Логин (OAuth2: username = email)
    login_response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": "test1@example.com",  # ← username, не email!
            "password": "testpassword",
        },
    )
    
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient):
    """Проверка входа с неверным паролем"""
    
    # Регистрация (уникальный email!)
    register_response = await client.post(
        "/api/v1/users/register",
        json={
            "email": "test2@example.com",
            "password": "testpassword",
        },
    )
    assert register_response.status_code in (200, 201)
    
    # Логин с неправильным паролем
    response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": "test2@example.com",
            "password": "wrongpassword",
        },
    )
    
    assert response.status_code == 401
    
    