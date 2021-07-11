from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, validator, Field

from .user_schemas import PostUser


# Post block
class PostBase(BaseModel):
    text: str


class PostCreateOrUpdate(PostBase):
    group_id: Optional[int] = None


class Post(PostBase):
    id: int
    author: Union[str, PostUser] = Field(alias='author')
    group_id: Optional[int] = None
    pub_date: datetime

    class Config:
        orm_mode = True

    @validator('author', always=True, pre=True)
    def validate_author_username(cls, v):
        return v.username


# Group block
class GroupBase(BaseModel):
    title: str


class GroupCreateOrUpdate(GroupBase):
    pass


class Group(GroupBase):
    id: int
    author: Union[PostUser, str]

    class Config:
        orm_mode = True

    @validator('author', always=True, pre=True)
    def validate_author_username(cls, v):
        return v.username


# Comment block
class CommentBase(BaseModel):
    text: str


class CommentCreateOrUpdate(CommentBase):
    pass


class Comment(CommentBase):
    id: int
    author: Union[PostUser, str]
    created: datetime
    post_id: int

    class Config:
        orm_mode = True

    @validator('author', always=True, pre=True)
    def validate_author_username(cls, v):
        return v.username


# Follow block
class FollowBase(BaseModel):
    following_id: int


class FollowCreate(FollowBase):
    pass


class Follow(FollowBase):
    follows_id: int
    user_id: int

    class Config:
        orm_mode = True
