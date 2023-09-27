from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app import schemas, models, oauth2, utils
from app.database import get_db

router = APIRouter(
    prefix="/follow",
    tags=["follow"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def follow_user(follow: schemas.Follow, db: Session = Depends(get_db),
                current_user: schemas.User = Depends(
                    oauth2.get_current_active_user)
                ):
    # check to ensure user only follows or unfollows other users
    if current_user.id == follow.followed_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user can only follow or unfollow other users"
        )

    # check if the user exists
    user = utils.find_user_by_id(follow.followed_id, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {follow.followed_id} was not found")

    follow_query = db.query(models.Follow).filter(
        models.Follow.follower_id == current_user.id, models.Follow.followed_id == follow.followed_id)
    found_follow = follow_query.first()

    if follow.dir == 1:
        if found_follow:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"you already follow user with id: {follow.followed_id}")
        new_follow = models.Follow(follower_id=current_user.id,
                                   followed_id=follow.followed_id)
        db.add(new_follow)
        db.commit()
        return {"message": "followed successfully"}

    else:
        if not found_follow:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"you don't follow user with id: {follow.followed_id}")
        follow_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "unfollowed successfully"}
