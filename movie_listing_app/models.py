from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from movie_listing_app.database import Base
import datetime

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default="user")

    ratings = relationship('Rating', back_populates='user')
    comments = relationship('Comment', back_populates='user')
    movies = relationship('Movie', back_populates='owner')


class Movie(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    release_year = Column(Integer)
    genre = Column(String)
    rating = Column(Float)
    synopsis = Column(Text)
    owner_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship('User', back_populates='movies')
    ratings = relationship('Rating', back_populates='movie')
    comments = relationship('Comment', back_populates='movie')


class Rating(Base):
    __tablename__ = 'ratings'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    movie_id = Column(Integer, ForeignKey('movies.id'), nullable=False)
    rating = Column(Integer, nullable=False)
    review = Column(Text)

    user = relationship('User', back_populates='ratings')
    movie = relationship('Movie', back_populates='ratings')




class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    movie_id = Column(Integer, ForeignKey('movies.id'), nullable=False)
    comment = Column(Text, nullable=False)
    parent_comment_id = Column(Integer, ForeignKey('comments.id'), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.now)

    user = relationship('User', back_populates='comments')
    movie = relationship('Movie', back_populates='comments')
    parent_comment = relationship('Comment', remote_side=[id], back_populates='replies')
    replies = relationship('Comment', back_populates='parent_comment', cascade='all, delete-orphan')
