from .. import models, schemas, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi import Depends, status, APIRouter, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from typing import Annotated

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # check if the user has registered before
    is_registered_user = db.query(models.User).filter(
        models.User.email == user.email).first()
    if is_registered_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="email already associated with a user")

    # check if the phone number is unique to user
    phone_number_exists = db.query(models.User).filter(
        models.User.phone_number == user.phone_number).first()
    if phone_number_exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="phone number already associated with a user")

    # check if the username is unique to user
    username_exists = db.query(models.User).filter(
        models.User.username == user.username).first()
    if username_exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="username already associated with a user")

    # hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login", response_model=schemas.Token)
def login_user(user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
               db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = oauth2.create_access_token(
        data={"user_id": user.id}, expires_in=oauth2.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/logout")
def logout_user(user: Annotated[schemas.User, Depends(oauth2.get_current_active_user)]):
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
