from pydantic import Field, ConfigDict, BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from typing_extensions import Annotated


class UserBase(BaseModel):
    email: EmailStr
    phone_number: Optional[str]


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    user_id: int
    model_config = ConfigDict(from_attributes=True)


class PostJoin(BaseModel):
    Post: Post
    like_count: int
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


class Like(BaseModel):
    post_id: int
    dir: Annotated[int, Field(ge=0, le=1)]
