import datetime
from fastapi import HTTPException
from starlette import status
from sqlalchemy import func
from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# User CRUD operations
def get_user(db: Session, user_id: int):
    """
    Fetches a user.

    :param db: SQLAlchemy database session.
    :param user_id: user ID.
    :return: first User with the ID once found.
    """
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    """
    Fetches a user by their username.

    :param db: SQLAlchemy database session.
    :param user_id: user ID.
    :return: first User with the username once found.
    """
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    """
    Fetches a user by their email.

    :param db: SQLAlchemy database session.
    :param user_id: user ID.
    :return: first User with the email once found.
    """
    return db.query(models.User).filter(models.User.email == email).first()

# function to create a user.
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)  # This encrypts the password
    db_user = models.User(
        username=user.username,
        email=user.email,
        password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        role='user'  # Default role for new users
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Movie CRUD operations
def get_movie_by_id(db: Session, movie_id: int):
    """
    Fetches a movie by ID.

    :param db: SQLAlchemy database session.
    :param movie_id: Optional movie ID.
    :param title: Optional movie title.
    :return: Movie object.
    """
    return db.query(models.Movie).filter(models.Movie.id == movie_id).first()

def get_all_movies(db: Session, skip: int = 0, limit: int = 10):
    """
    Fetches all movies with a limit(optional) and skip(optional).

    :param db: SQLAlchemy database session.
    :return: Movie object with the set limit and skip.
    """
    return db.query(models.Movie).offset(skip).limit(limit).all()

def get_movie_by_title(db: Session, title: str):
    """
    Fetches a movie by title regardless of the case(i.e it is case insensitive)

    :param db: SQLAlchemy database session.
    :param movie_title: movie title.
    :param title: Optional movie title.
    :return: Movie object.
    """
    return db.query(models.Movie).filter(func.lower(models.Movie.title) == func.lower(title)).first()

def get_movie_by_release_year(db: Session, release_year: int):
    return db.query(models.Movie).filter(models.Movie.release_year == release_year).first()

# this funcion is used to create a movie
def create_movie(db: Session, movie: schemas.MovieCreate, user_id: int):
    db_movie = models.Movie(**movie.model_dump(), owner_id=user_id)
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

# this funcion is used to update the details of a movie whilst filtering by the movie id
def update_movie_by_id(db: Session, movie_id: int, movie: schemas.MovieCreate):
    db_movie = get_movie_by_id(db, movie_id)
    if not db_movie:
        return None
    for key, value in movie.model_dump().items():
        setattr(db_movie, key, value)
    db.commit()
    db.refresh(db_movie)
    return db_movie

# this funcion is used to delete a movie oncec it is found, using the movie id to search
def delete_movie_by_id(db: Session, movie_id: int):
    db_movie = get_movie_by_id(db, movie_id)
    if db_movie:
        db.delete(db_movie)
        db.commit()
    return db_movie

# this funcion is used to update the details of a movie whilst filtering by the movie title
def update_movie_by_title(db: Session, movie_title: str, movie: schemas.MovieCreate):
    db_movie = get_movie_by_title(db, movie_title)
    if not db_movie:
        return None
    for key, value in movie.model_dump().items():
        setattr(db_movie, key, value)
    db.commit()
    db.refresh(db_movie)
    return db_movie

# this funcion is used to delete a movie oncec it is found, using the movie title to search
def delete_movie_by_title(db: Session, movie_title: str):
    db_movie = get_movie_by_title(db, movie_title)
    if db_movie:
        db.delete(db_movie)
        db.commit()
    return db_movie
# Rating CRUD operations
def get_rating(db: Session, rating_id: int):
    return db.query(models.Rating).filter(models.Rating.id == rating_id).first()

def get_ratings_by_movie(db: Session, movie_id: int):
    return db.query(models.Rating).filter(models.Rating.movie_id == movie_id).all()

def get_ratings_by_user(db: Session, user_id: int):
    return db.query(models.Rating).filter(models.Rating.user_id == user_id).all()

def get_ratings_by_score(db: Session, score: int):
    return db.query(models.Rating).filter(models.Rating.rating == score).all()

def create_rating(db: Session, rating: schemas.RatingCreate, user_id: int):
    db_rating = models.Rating(
        rating=rating.rating,
        review=rating.review,
        user_id=user_id,
        movie_id=rating.movie_id 
    )
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    update_movie_rating(db, rating.movie_id)
    return db_rating

def create_rating_by_title(db: Session, rating: schemas.RatingCreate, user_id: int, title: str):
    movie = get_movie_by_title(db=db, title=title)
    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    
    db_rating = models.Rating(
        rating=rating.rating,
        review=rating.review,
        user_id=user_id,
        movie_id=movie.id
    )
    
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    update_movie_rating_by_title(db=db, movie=movie)
    return db_rating


def update_movie_rating(db: Session, movie_id: int):
    avg_rating = db.query(func.avg(models.Rating.rating)).filter(models.Rating.movie_id == movie_id).scalar()
    db_movie = get_movie_by_id(db, movie_id)
    if db_movie:
        db_movie.rating = avg_rating
        db.commit()
        db.refresh(db_movie)

def update_movie_rating_by_title(db: Session, movie: models.Movie):
    # Calculate the average rating
    avg_rating = db.query(func.avg(models.Rating.rating)).filter(models.Rating.movie_id == movie.id).scalar()
    movie.rating = avg_rating
    db.commit()
    db.refresh(movie)
    


def delete_rating(db: Session, rating_id: int):
    db_rating = get_rating(db, rating_id)
    if db_rating:
        db.delete(db_rating)
        db.commit()
        update_movie_rating(db, db_rating.movie_id) # type: ignore
    return db_rating

# Comment CRUD operations
def get_comment(db: Session, comment_id: int):
    return db.query(models.Comment).filter(models.Comment.id == comment_id).first()


def create_comment(db: Session, comment: schemas.CommentCreate, user_id: int):
    db_comment = models.Comment(
        comment=comment.comment,
        user_id=user_id,
        movie_id=comment.movie_id,
        parent_comment_id=comment.parent_comment_id if comment.parent_comment_id else None,
        created_at=datetime.datetime.now()
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def get_comments_by_movie(db: Session, movie_id: int):
    return db.query(models.Comment).filter(models.Comment.movie_id == movie_id).all()

def get_comments_by_user(db: Session, user_id: int):
    return db.query(models.Comment).filter(models.Comment.user_id == user_id).all()