from pydantic import Field, ConfigDict, BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from typing_extensions import Annotated


class UserBase(BaseModel):
    email: EmailStr
    phone_number: str
    name: str
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    created_at: datetime
    bio: str | None
    cover_image: str | None
    profile_image: str | None
    updated_at: datetime | None
    model_config = ConfigDict(from_attributes=True)


class UserJoin(BaseModel):
    User: User
    follower_count: int


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    phone_number: str | None = None
    name: str | None = None
    username: str | None = None
    bio: str | None = None
    cover_image: str | None = None
    profile_image: str | None = None


class PostCreate(BaseModel):
    content: str
    published: bool = True


class Post(PostCreate):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime | None
    model_config = ConfigDict(from_attributes=True)


class PostJoin(BaseModel):
    Post: Post
    like_count: int
    model_config = ConfigDict(from_attributes=True)


class PostUpdate(BaseModel):
    content: str | None = None
    published: bool | None = None


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


class Like(BaseModel):
    post_id: int
    dir: Annotated[int, Field(ge=0, le=1)]


class Follow(BaseModel):
    followed_id: int
    dir: Annotated[int, Field(ge=0, le=1)]
