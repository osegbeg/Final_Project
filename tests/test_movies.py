# tests/test_movies.py

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
async def test_create_movie():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/auth/login", data={
            "username": "testuser4",
            "password": "password123"
        })
        token = response.json()["access_token"]

        response = await ac.post("/movies/", json={
            "title": "Inception",
            "release_year": 2010,
            "genre": "Sci-Fi",
            "synopsis": "A thief who steals corporate secrets through the use of dream-sharing technology..."
        }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    assert response.json()["title"] == "Inception"

@pytest.mark.asyncio
async def test_get_movies():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/movies/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
