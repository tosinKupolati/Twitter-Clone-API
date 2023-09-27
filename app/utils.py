from sqlalchemy.orm import Session
from passlib.context import CryptContext
from . import models
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def find_post_by_id(id: int, db: Session):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    return post


def find_user_by_id(id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    return user
