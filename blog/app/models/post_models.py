import datetime as dt
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Table
from sqlalchemy.sql.schema import CheckConstraint, UniqueConstraint

from ..database import Base


class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    author_id = Column('User', ForeignKey('users.id'), nullable=False)
    title = Column(String(50), index=True, nullable=False, unique=True)

    author = relationship('User', back_populates='group')
    posts = relationship('Post', back_populates='group')


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    text = Column(String, index=True, nullable=False)
    author_id = Column('User', ForeignKey('users.id'), nullable=False)
    group_id = Column('Group', ForeignKey('groups.id'), nullable=True)
    pub_date = Column(DateTime, default=dt.datetime.now)

    author = relationship('User', back_populates='posts')
    group = relationship('Group', back_populates='posts')
    comments = relationship(
        'Comment', back_populates='post'
    )

    def __repr__(self):
        return f'<Post(text={self.text[:20]})>'


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    text = Column(String, index=True, nullable=False)
    author_id = Column('User', ForeignKey('users.id'))
    post_id = Column('Post', ForeignKey('posts.id'))
    created = Column(DateTime, default=dt.datetime.now)

    author = relationship('User', back_populates='comments')
    post = relationship('Post', back_populates='comments', cascade='all, delete')

    def __repr__(self):
        return f'<Commens(post={self.post_id}), text={self.text[:20]}>'


follow_table = Table(
    'follows', Base.metadata,
    Column('follows_id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id'), nullable=False),
    Column('following_id', Integer, ForeignKey('users.id'), nullable=False),
    UniqueConstraint('user_id', 'following_id', name='unique_follow'),
    CheckConstraint('user_id != following_id', name='user_is_not_author')
)


class Follow(Base):
    __table__ = follow_table
