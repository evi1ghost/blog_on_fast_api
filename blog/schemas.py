from datetime import datetime
# from typing import List, Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    # posts: List[Post] = []

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    text: str


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    author_id: int
    group_id: int
    pub_date: datetime

    class Config:
        orm_mode = True


class GroupBase(BaseModel):
    title: str


class GroupCreate(GroupBase):
    pass


class Group(GroupBase):
    id: int

    class Config:
        orm_mode = True


class CommentBase(BaseModel):
    text: str


class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    id: int
    author_id: int
    created: datetime
    post_id: int

    class Config:
        orm_mode = True


class FollowBase(BaseModel):
    user_id: int
    following_id: int

    class Config:
        orm_mode = True


class FollowCreate(FollowBase):
    pass


class Follow(FollowBase):
    id: int
