from sqlalchemy import Boolean, Column, Integer, String, TIMESTAMP, ForeignKey
from .database import Base
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    phone_number = Column(String, unique=True)
    # relationships using attributes
    posts = relationship("Post", back_populates="user")
    likes = relationship("Like", back_populates="user")


class Post(Base):

    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, server_default='True')
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    # relationships using attributes
    user = relationship("User", back_populates="posts")
    likes = relationship("Like", back_populates="post")


class Like(Base):

    __tablename__ = "likes"

    post_id = Column(Integer, ForeignKey(
        "posts.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), primary_key=True)
    post = relationship("Post", back_populates="likes")
    user = relationship("User", back_populates="likes")
