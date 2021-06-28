import datetime as dt
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import CheckConstraint, UniqueConstraint

from .database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    posts = relationship('Post', back_populates="author")

    def __repr__(self):
        return f'<User(username={self.username})>'


class Group(Base):
    __tablename___ = 'groups'

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    text = Column(String, index=True, nullable=False)
    author_id = Column('User', ForeignKey('user.id'))
    group_id = Column('Group', ForeignKey('group.id'))
    pub_date = Column(DateTime, default=dt.datetime)

    author = relationship('User', back_populates='posts')
    group = relationship('Group', back_populates='posts')

    def __repr__(self):
        return f'<Post(text={self.text[:20]})>'


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    text = Column(String, index=True, nullable=False)
    author_id = Column('User', ForeignKey('user.id'))
    post_id = Column('Post', ForeignKey('post.id'))
    created = Column(DateTime, default=dt.datetime)

    author = relationship('User', back_populates='comments')
    post = relationship('Post', back_populates='comments')

    def __repr__(self):
        return f'<Commens(post={self.post_id}), text={self.text[:20]}>'


class Follow(Base):
    __tablename__ = 'follows'
    __table_args__ = (
        CheckConstraint('user_id != following_id', name='user_is_not_author'),
        UniqueConstraint('user_id', 'following_id', name='unique_follow'),
    )

    id = Column(Integer, primary_key=True)
    user_id = Column('User', ForeignKey('user.id'))
    following_id = Column('User', ForeignKey('user.id'))

    user = relationship('User', back_populates='follower')
    following = relationship('User', back_populates='following')

    def __repr__(self):
        return f'<Follow(user={self.user_id}), following={self.following_id}>'
