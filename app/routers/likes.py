from fastapi import Depends, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List, Annotated
from .. import models, schemas, oauth2, utils

router = APIRouter(prefix="/like", tags=["Like"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def like(like: schemas.Like, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    post = utils.find_post_by_id(like.post_id, db)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {like.post_id} cannot be found")

    like_query = db.query(models.Like).filter(
        models.Like.post_id == like.post_id, models.Like.user_id == current_user.id)
    found_like = like_query.first()

    if like.dir == 1:
        if found_like:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user with id {current_user.id} has already liked this post with id {like.post_id}")

        new_like = models.Like(post_id=like.post_id, user_id=current_user.id)
        db.add(new_like)
        db.commit()
        return {"message": "successfully liked this post"}
    else:
        if not found_like:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"no like has been found for user with id {current_user.id}")
        like_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted like for this post"}
