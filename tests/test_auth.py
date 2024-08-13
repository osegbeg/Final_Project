# tests/test_auth.py

import pytest
from httpx import AsyncClient
from movie_listing_app.main import app
from tests.test_database import get_test_db, Base, engine
from movie_listing_app.dependencies import get_db

# Override the get_db dependency to use the test database
app.dependency_overrides[get_db] = get_test_db

# Create the test database tables
Base.metadata.create_all(bind=engine)

@pytest.mark.asyncio
async def test_register_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/auth/register", json={
            "first_name": "test",
            "last_name": "user3",
            "username": "testuser3",
            "email": "testuser3@example.com",
            "password": "password123"
        })
    assert response.status_code == 201
    assert response.json()["username"] == "testuser3"

@pytest.mark.asyncio
async def test_login_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/auth/login", data={
            "username": "testuser3",
            "password": "password123"
        })
    assert response.status_code == 200
    assert "access_token" in response.json()
