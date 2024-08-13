import logging
from fastapi import FastAPI
from .routers import auth, movies, ratings, comments
from .database import engine, Base
from movie_listing_app.logging_config import configure_logging

configure_logging()

app = FastAPI()

app.include_router(auth.router)
app.include_router(movies.router)
app.include_router(ratings.router)
app.include_router(comments.router)

Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root_endpoint():
    logging.info("Accessing the root endpoint was successful")
    return {"message": "Welcome to the Movie Listing API"}
