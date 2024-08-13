import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, models, crud, dependencies
from movie_listing_app.logging_config import configure_logging

router = APIRouter(
    prefix="/comments",
    tags=["comments"],
)

configure_logging()


# endpoint to create comment by movie ID
@router.post("/", response_model=schemas.Comment, status_code=status.HTTP_201_CREATED)
def create_comment(
    comment: schemas.CommentCreate,
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.get_current_user)
):
    db_movie = crud.get_movie_by_id(db, movie_id=comment.movie_id)
    if not db_movie:
        logging.warning("movie not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    logging.info(f"user: {current_user.username} commented on movie: {db_movie.title}")
    return crud.create_comment(db=db, comment=comment, user_id=current_user.id) # type: ignore

# if a user does not know the movie ID, this is an endpoint to create comment by movie title
@router.post("/by-title/", response_model=schemas.Comment)
def create_comment_by_title(
    comment: schemas.CommentBase,
    movie_title: str,
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.get_current_user)
):
    db_movie = crud.get_movie_by_title(db, title=movie_title)
    if not db_movie:
        logging.warning("movie not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    comment_create = schemas.CommentCreate(
        comment=comment.comment,
        movie_id=db_movie.id, # type: ignore
        parent_comment_id=None 
    )
    logging.info(f"user: {current_user.username} commented on movie: {db_movie.title}")
    return crud.create_comment(db=db, comment=comment_create, user_id=current_user.id) # type: ignore

# endpoint to get all comments by movie ID
@router.get("/movie/{movie_id}", response_model=List[schemas.Comment])
def read_comments_by_movie(movie_id: int, db: Session = Depends(dependencies.get_db)):
    logging.info(f"reading comments for movie: {movie_id}")
    return crud.get_comments_by_movie(db, movie_id=movie_id)

# endpoint to get all comments by movie title
@router.get("/by-title/{movie_title}", response_model=List[schemas.Comment])
def read_comments_by_movie_title(movie_title: str, db: Session = Depends(dependencies.get_db)):
    logging.info(f"Fetching comments for movie '{movie_title}'")
    movie = crud.get_movie_by_title(db=db, title=movie_title)
    if not movie:
        logging.error(f"Movie not found for title '{movie_title}' during comment retrieval")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    
    comments = crud.get_comments_by_movie(db=db, movie_id=movie.id) # type: ignore
    logging.info(f"Retrieved {len(comments)} comments for movie '{movie.title}'")
    return comments

