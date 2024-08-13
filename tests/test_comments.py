# tests/test_comments.py

import pytest
from httpx import AsyncClient
from movie_listing_app.main import app
from tests.test_database import get_test_db, Base, engine
from sqlalchemy.orm import Session
from movie_listing_app.dependencies import get_db
from movie_listing_app import models

# Override the get_db dependency to use the test database
app.dependency_overrides[get_db] = get_test_db

# Create the test database tables
Base.metadata.create_all(bind=engine)

@pytest.mark.asyncio
async def test_create_comment():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/auth/login", data={
            "username": "testuser3",
            "password": "password123"
        })
        token = response.json()["access_token"]

        response = await ac.get("/movies/")
        movie_id = response.json()[0]["id"]

        response = await ac.post("/comments/", json={
            "comment": "Great movie!",
            "movie_id": movie_id
        }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    assert response.json()["comment"] == "Great movie!"

@pytest.mark.asyncio
async def test_get_comments_by_movie():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/movies/")
        movie_id = response.json()[0]["id"]

        response = await ac.get(f"/comments/movie/{movie_id}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)



@pytest.mark.asyncio
async def test_read_comments_by_movie_title(db: Session):
    # Create a user and a movie for testing
    test_user = models.User(
        first_name="Test",
        last_name="User",
        username="testuser1",
        email="testuser1@example.com",
        password="password123"
    )
    db.add(test_user)
    db.commit()
    db.refresh(test_user)

    test_movie = models.Movie(
        title="Inception",
        release_year=2010,
        genre="Sci-Fi",
        synopsis="A thief who steals corporate secrets through dream-sharing technology.",
        owner_id=test_user.id
    )
    db.add(test_movie)
    db.commit()
    db.refresh(test_movie)

    # Add some comments to the movie
    comment1 = models.Comment(
        comment="Amazing movie!",
        user_id=test_user.id,
        movie_id=test_movie.id
    )
    comment2 = models.Comment(
        comment="A masterpiece by Christopher Nolan.",
        user_id=test_user.id,
        movie_id=test_movie.id
    )
    db.add_all([comment1, comment2])
    db.commit()

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/comments/by-title/{test_movie.title}")

    assert response.status_code == 200
    comments = response.json()
    assert len(comments) == 2
    assert comments[0]["comment"] == "Amazing movie!"
    assert comments[1]["comment"] == "A masterpiece by Christopher Nolan."

    # Test with a non-existent movie title
    response = await ac.get("/comments/by-title/NonExistentMovie")
    assert response.status_code == 404
    assert response.json()["detail"] == "Movie not found"
