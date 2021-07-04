import datetime as dt
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Table
from sqlalchemy.sql.schema import CheckConstraint, UniqueConstraint

from ..database import Base


class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    title = Column(String(50), index=True, nullable=False)

    posts = relationship('Post', back_populates='group')


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


follow_table = Table(
    'follows', Base.metadata,
    Column('follows_id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey('user.id'), nullable=False),
    Column('following_id', Integer, ForeignKey('user_id'), nullable=False),
    UniqueConstraint('user_id', 'following_id', name='unoque_follow'),
    CheckConstraint('user_id != following_id', name='user_is_not_author')
)
