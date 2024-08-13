import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, models, crud, dependencies
from movie_listing_app.logging_config import configure_logging

router = APIRouter(
    prefix="/movies",
    tags=["movies"],
)
configure_logging()

# endpoint for listing a new movie
@router.post("/", response_model=schemas.Movie, status_code=status.HTTP_201_CREATED)
def create_movie(movie: schemas.MovieCreate, db: Session = Depends(dependencies.get_db), 
                 current_user: models.User = Depends(dependencies.get_current_user)):
    logging.info(f"Movie created: {movie.title} by user {current_user.username}")
    return crud.create_movie(db=db, movie=movie, user_id=current_user.id) # type: ignore

# endpoint for retrieving all movies
@router.get("/", response_model=List[schemas.Movie])
def read_movies(skip: int = 0, limit: int = 10, db: Session = Depends(dependencies.get_db)):
    movies = crud.get_all_movies(db, skip=skip, limit=limit)
    logging.info("user tried to get all movies and found them")
    return movies

# endpoint for retrieving a single movie by title
@router.get("/{title}", response_model=schemas.Movie)
def read_movie(movie_title: str, db: Session = Depends(dependencies.get_db)):
    db_movie = crud.get_movie_by_title(db, title=movie_title)
    if db_movie is None:
        logging.warning("movie not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    logging.info(f"user viewed movie: {db_movie.title}")
    return db_movie


# endpoint for retrieving movies by release year
@router.get("/search/{release_year}", response_model=schemas.Movie)
def read_movie_by_release_year(release_year: int, db: Session = Depends(dependencies.get_db)):
    db_movie = crud.get_movie_by_release_year(db, release_year=release_year)
    if db_movie is None:
        logging.warning("movie not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Movie not found")
    logging.info(f"user viewed movie: {db_movie.title}")
    return db_movie

# endpoint for making updates to listed movies, current user dependency injection in place.
@router.put("/{movie_id}", response_model=schemas.Movie)
def update_movie(movie_id: int, movie: schemas.MovieCreate, db: Session = Depends(dependencies.get_db), current_user: models.User = Depends(dependencies.get_current_user)):
    db_movie = crud.get_movie_by_id(db, movie_id=movie_id)
    if db_movie is None:
        logging.warning("movie not found, failed to update")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    if db_movie.owner_id != current_user.id: # type: ignore
        logging.warning("Unauthorized movie update attempt by user")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this movie")
    logging.info(f"Movie updated: {movie.title} by user {current_user.username}")
    return crud.update_movie_by_id(db, movie_id=movie_id, movie=movie)

# endpoint for deleting listed movies, current user dependency injection in place.
@router.delete("/{movie_id}", response_model=schemas.Movie)
def delete_movie(movie_id: int, db: Session = Depends(dependencies.get_db), current_user: models.User = Depends(dependencies.get_current_user)):
    db_movie = crud.get_movie_by_id(db, movie_id=movie_id)
    if db_movie is None:
        logging.warning("movie not found, failed to delete")
        raise HTTPException(status_code=404, detail="Movie not found")
    if db_movie.owner_id != current_user.id: # type: ignore
        logging.warning(f"Unauthorized movie deletion attempt by user {current_user.username}")
        raise HTTPException(status_code=403, detail="Not authorized to delete this movie")
    logging.info(f"Movie deleted: {db_movie.title} by user {current_user.username}")
    return crud.delete_movie_by_id(db, movie_id=movie_id)
