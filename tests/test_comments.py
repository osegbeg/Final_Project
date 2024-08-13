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

