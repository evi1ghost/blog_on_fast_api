from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from ..database import Base
from ..models.post_models import follow_table


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    posts = relationship(
        'Post', back_populates="author",
        cascade="all, delete, delete-orphan"
    )
    comments = relationship(
        'Comment', back_populates='author',
        cascade="all, delete, delete-orphan"
    )
    follower = relationship(
        'Follow',
        secondary=follow_table,
        back_populates='user',
        cascade="all, delete, delete-orphan"
    )
    following = relationship(
        'Follow',
        secondary=follow_table,
        back_populates='following',
        cascade="all, delete, delete-orphan"
    )

    def __repr__(self):
        return f'<User(username={self.username})>'
