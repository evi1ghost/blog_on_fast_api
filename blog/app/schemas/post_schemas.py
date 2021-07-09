from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PostBase(BaseModel):
    text: str


class PostCreateOrUpdate(PostBase):
    group_id: Optional[int] = None


class Post(PostBase):
    id: int
    author_id: int
    group_id: Optional[int] = None
    pub_date: datetime

    class Config:
        orm_mode = True


class GroupBase(BaseModel):
    title: str


class GroupCreateOrUpdate(GroupBase):
    pass


class Group(GroupBase):
    id: int
    author_id: int

    class Config:
        orm_mode = True


class CommentBase(BaseModel):
    text: str


class CommentCreateOrUpdate(CommentBase):
    pass


class Comment(CommentBase):
    id: int
    author_id: int
    created: datetime
    post_id: int

    class Config:
        orm_mode = True


class FollowBase(BaseModel):
    following_id: int


class FollowCreate(FollowBase):
    pass


# Добавить валидацию


class Follow(FollowBase):
    follows_id: int
    user_id: int

    class Config:
        orm_mode = True
