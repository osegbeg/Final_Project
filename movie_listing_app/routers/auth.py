import logging
import os
from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Annotated, Optional
from sqlalchemy.orm import Session
from .. import schemas, models, crud, dependencies
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from dotenv import load_dotenv
from movie_listing_app.logging_config import configure_logging


load_dotenv()
configure_logging()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# created a verify password function
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# here is the function to get the hashed password
def get_password_hash(password):
    return pwd_context.hash(password)

# function to create JWT access token
def create_access_token(data: dict, expires_delta: timedelta = None): # type: ignore
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) # type: ignore
    return encoded_jwt

# movie_listing_app/routers/auth.py
## endpoint to register new user
@router.post("/register", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def register_user(user_create: schemas.UserCreate, db: Session = Depends(dependencies.get_db)):
    hashed_password = get_password_hash(user_create.password)
    logging.info(f"Registering user: {user_create.username}, Hashed Password: {hashed_password}") 
    create_user_model = models.User(
        first_name=user_create.first_name,
        last_name=user_create.last_name,
        username=user_create.username,
        email=user_create.email,
        password=hashed_password
    )
    db_user = crud.create_user(db=db, user=create_user_model)
    logging.info(f"New user registered: {db_user.username}")
    return db_user

## endpoint for user login, it returns the JWT bearer token upon successful login
@router.post("/login", response_model=schemas.Token)
def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(dependencies.get_db)):
    db_user = crud.get_user_by_username(db, username=form_data.username)
    if db_user:
        logging.info(f"User found: {db_user.username}, Hashed Password: {db_user.password}")  
        
    else:
        logging.warning(f"User not found: {form_data.username}")  

    if not db_user or not verify_password(form_data.password, db_user.password):
        logging.warning(f"Failed login attempt for user: {form_data.username}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.username}, expires_delta=access_token_expires
    )
    logging.info(f"User logged in: {db_user.username}")
    return {"access_token": access_token, "token_type": "bearer"}
