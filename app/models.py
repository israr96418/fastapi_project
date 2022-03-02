from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    Name = Column(String(30), nullable=True)
    experience = Column(String(70), nullable=True)
    Email = Column(String(30), unique=True, nullable=False)
    password = Column(String(300), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=True, server_default=text('now()'))


class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True, nullable=False)
    Name = Column(String(30), nullable=True)
    Email = Column(String(30), nullable=True)
    Address = Column(String(255), nullable=True)
    is_active = Column(Boolean, nullable=True)
    password = Column(String(200), nullable=True)
    last_name = Column(String(20), nullable=True)

    #     (one to many) relationship with user..Means user create many post but post only related with one user
    owner_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    # phone_number = Column(String(30))

    # return model(sqlalchemy model)
    # owner = relationship("User")


# composite key (user_id, post_id)
class Vote(Base):
    __tablename__="vote"
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    post_id = Column(Integer, ForeignKey("post.id", ondelete="CASCADE"), primary_key=True, nullable=False)