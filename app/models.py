from sqlalchemy import Boolean, Column, Integer, String, TIMESTAMP, ForeignKey
from .database import Base
from sqlalchemy.sql.expression import text


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    phone_number = Column(String, unique=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True))
    bio = Column(String)
    email_verified = Column(Boolean, server_default='False')
    cover_image = Column(String)
    profile_image = Column(String)
    has_notification = Column(Boolean)
    is_active = Column(Boolean, nullable=False, server_default='True')


class Post(Base):

    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, server_default='True')
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True))
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)


class Like(Base):

    __tablename__ = "likes"

    post_id = Column(Integer, ForeignKey(
        "posts.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False, primary_key=True)


class Comment(Base):

    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, nullable=False)
    post_id = Column(Integer, ForeignKey(
        "posts.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True))


class Notification(Base):

    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, nullable=False)
    content = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True))


class Follow(Base):

    __tablename__ = "follows"

    follower_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    followed_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False, primary_key=True)
