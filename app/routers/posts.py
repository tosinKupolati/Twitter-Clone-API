from fastapi import Depends, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List, Annotated
from .. import models, schemas, oauth2
from sqlalchemy import select
from datetime import datetime
from sqlalchemy.sql.expression import func


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/", response_model=List[schemas.PostJoin])
def get_posts(
    db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = ""
):
    skip = (page-1)*limit

    posts = db.execute(
        select(models.Post, func.count(models.Like.post_id).label("like_count")).
        join(models.Like, models.Post.id == models.Like.post_id, isouter=True).
        group_by(models.Post.id).filter(models.Post.content.contains(search)).
        offset(skip).limit(limit)
    ).all()

    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(
    user: Annotated[schemas.User, Depends(oauth2.get_current_active_user)],
    post: schemas.PostCreate, db: Session = Depends(get_db)
):
    new_post = models.Post(user_id=user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.PostJoin)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post, func.count(models.Like.post_id).label("like_count")).join(
        models.Like, models.Post.id == models.Like.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(user: Annotated[schemas.User, Depends(oauth2.get_current_active_user)], id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    if post.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="not authorized to perform requested action")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(
        user: Annotated[schemas.User, Depends(oauth2.get_current_active_user)],
        id: int, updated_post: schemas.PostUpdate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    if post.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="not authorized to perform requested action")

    if updated_post.content:
        post_query.update({"content": updated_post.content},
                          synchronize_session=False)

    if updated_post.published:
        if not post.published:
            post_query.update(
                {"published": updated_post.published}, synchronize_session=False)

    post_query.update({"updated_at": datetime.now()},
                      synchronize_session=False)

    db.commit()
    return post_query.first()
