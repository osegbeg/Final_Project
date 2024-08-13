from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class MovieBase(BaseModel):
    title: str
    release_year: Optional[int] = None
    genre: Optional[str] = None
    synopsis: Optional[str] = None

class MovieCreate(MovieBase):
    pass

class Movie(MovieBase):
    id: int
    rating: Optional[float] = None
    owner_id: int
    owner: User

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

class RatingBase(BaseModel):
    rating: int
    review: Optional[str] = None

class RatingCreate(RatingBase):
    movie_id: int

class Rating(RatingBase):
    id: int
    user_id: int
    movie_id: int
    user: User
    movie: Movie

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

class CommentBase(BaseModel):
    comment: str

class CommentCreate(CommentBase):
    movie_id: int  
    parent_comment_id: Optional[int] = None

class Comment(CommentBase):
    id: int
    user_id: int
    movie_id: int
    created_at: datetime
    user: User
    movie: Movie
    parent_comment: Optional["Comment"] = None
    replies: List["Comment"] = []

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

# Enable forward references for nested comments
Comment.model_rebuild()
