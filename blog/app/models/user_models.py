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
        'Post', back_populates='author',
        cascade='all, delete'
    )
    comments = relationship(
        'Comment', back_populates='author',
        cascade='all, delete'
    )
    follower = relationship(
        'User', lambda: follow_table,
        primaryjoin=lambda: User.id == follow_table.c.user_id,
        secondaryjoin=lambda: User.id == follow_table.c.following_id,
        back_populates='follower',
        cascade='all, delete'
    )
    following = relationship(
        'User', lambda: follow_table,
        primaryjoin=lambda: User.id == follow_table.c.following_id,
        secondaryjoin=lambda: User.id == follow_table.c.user_id,
        back_populates='following',
        cascade='all, delete'
    )
    group = relationship(
        'Group', back_populates='author',
        cascade='all, delete'
    )

    def __repr__(self):
        return f'<User(username={self.username})>'
