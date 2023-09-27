from .. import models, schemas, oauth2
from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from sqlalchemy import func
from datetime import datetime

router = APIRouter(prefix="/users",
                   tags=['Users'])


@router.get("/current", response_model=schemas.UserJoin)
def show_current_user(current_user: schemas.User = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    user = db.query(models.User, func.count(models.Follow.followed_id).label("follower_count")).join(
        models.Follow, models.User.id == models.Follow.followed_id, isouter=True).group_by(models.User.id).filter(models.User.id == current_user.id).first()
    return user


@router.get("/{id}", response_model=schemas.UserJoin)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User, func.count(models.Follow.followed_id).label("follower_count")).join(
        models.Follow, models.User.id == models.Follow.followed_id, isouter=True).group_by(models.User.id).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} does not exist")
    return user


@router.put("/{id}", response_model=schemas.User)
def update_user(id: int, user_update: schemas.UserUpdate, current_user=Depends(oauth2.get_current_user), db=Depends(get_db)):

    current_email = current_user.email

    # check if user exists
    user_query = db.query(models.User).filter(models.User.id == id)
    if not user_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} does not exist")

    # check if user is authorized to update this user
    if current_user.id != id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="you are not authorized to update this user")

    if user_update.email:
        # check if email is unique
        email_exists = db.query(models.User).filter(
            models.User.email == user_update.email, models.User.id != id).first()
        if email_exists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="email already associated with another user")
        user_query.update({"email": user_update.email},
                          synchronize_session=False)

        # check if the new email is different from the old email
        if user_update.email != current_email:
            user_query.update({"email_verified": False},
                              synchronize_session=False)

    if user_update.phone_number:
        # check if phone_number is unique
        phone_number_exists = db.query(models.User).filter(
            models.User.phone_number == user_update.phone_number, models.User.id != id).first()
        if phone_number_exists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="phone number already associated with another user")
        user_query.update({"phone_number": user_update.phone_number},
                          synchronize_session=False)

    if user_update.username:
        # check if username is unique
        username_exists = db.query(models.User).filter(
            models.User.username == user_update.username, models.User.id != id).first()
        if username_exists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="username already associated with another user")
        user_query.update({"username": user_update.username},
                          synchronize_session=False)

    if user_update.name:
        user_query.update({"name": user_update.name},
                          synchronize_session=False)

    if user_update.bio:
        user_query.update({"bio": user_update.bio},
                          synchronize_session=False)

    if user_update.cover_image:
        user_query.update({"cover_image": user_update.cover_image},
                          synchronize_session=False)

    if user_update.profile_image:
        user_query.update({"profile_image": user_update.profile_image},
                          synchronize_session=False)

    user_query.update({"updated_at": datetime.now()})

    db.commit()
    return user_query.first()
