import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, models, crud, dependencies
from movie_listing_app.logging_config import configure_logging

router = APIRouter(
    prefix="/ratings",
    tags=["ratings"],
)

configure_logging()

# endpoint to rate a movie by movie id
@router.post("/", response_model=schemas.Rating, status_code=status.HTTP_201_CREATED)
def create_rating(
    rating: schemas.RatingCreate,
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.get_current_user)
):
    db_movie = crud.get_movie_by_id(db, movie_id=rating.movie_id)
    if not db_movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    logging.info(f"User created rating for movie with id: {db_movie}")
    return crud.create_rating(db=db, rating=rating, user_id=current_user.id) # type: ignore

# endpoint to rate a movie by title 
@router.post("/title/{title}/", response_model=schemas.Rating, status_code=status.HTTP_201_CREATED)
def create_rating_by_title(
    title: str,
    rating: schemas.RatingCreate,
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.get_current_user)
):
    logging.info(f"User {current_user.username} is creating a rating for movie '{title}'")
    return crud.create_rating_by_title(db=db, rating=rating, user_id=current_user.id, title=title) # type: ignore

# endpoint to get average ratings of a movie by movie id
@router.get("/movie_ratings/{movie_id}", response_model=List[schemas.Rating])
def read_ratings_by_movie(movie_id: int, db: Session = Depends(dependencies.get_db)):
    logging.info(f"User read ratings for movie with id: {movie_id}")
    return crud.get_ratings_by_movie(db, movie_id=movie_id)

# endpoint to get average ratings of a movie by title
@router.get("/by_title/{title}/", response_model=float) 
def get_average_rating_by_title(title: str, db: Session = Depends(dependencies.get_db)):
    logging.info(f"Fetching average rating for movie '{title}'")
    movie = crud.get_movie_by_title(db=db, title=title)
    if not movie:
        logging.error(f"Movie not found for title '{title}' during rating retrieval")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    
    avg_rating = movie.rating if movie.rating is not None else 0.0
    
    logging.info(f"Average rating for movie '{movie.title}' is {avg_rating}")
    return avg_rating

# endpoint to get the score for a movie
@router.get("/score/{score}", response_model=List[schemas.Rating])
def read_ratings_by_score(score: int, db: Session = Depends(dependencies.get_db)):
    logging.info(f"User read ratings with score: {score}")
    return crud.get_ratings_by_score(db, score=score)

# endpoint to delete a rating by rating id, current user dependency injection in place.
@router.delete("/{rating_id}", response_model=schemas.Rating)
def delete_rating(rating_id: int, db: Session = Depends(dependencies.get_db), current_user: models.User = Depends(dependencies.get_current_user)):
    db_rating = crud.get_rating(db, rating_id=rating_id)
    if db_rating is None or db_rating.user_id != current_user.id: # type: ignore
        logging.warning(f"Unauthorized movie deletion attempt by user {current_user.username}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this rating")
    logging.info(f"User deleted rating with id: {rating_id}")
    return crud.delete_rating(db, rating_id=rating_id)