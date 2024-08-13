# movie_listing_app/test_database.py

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from movie_listing_app.database import Base
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

engine = create_engine(TEST_DATABASE_URL) # type: ignore
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def get_test_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
