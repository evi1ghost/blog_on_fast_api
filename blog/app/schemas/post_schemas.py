from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, Field, validator

from ..crud.user_crud import get_user
from ..database import SessionLocal
from .user_schemas import PostUser


# Post block
class PostBase(BaseModel):
    text: str


class PostCreateOrUpdate(PostBase):
    group_id: Optional[int] = None


class Post(PostBase):
    id: int
    author: Union[str, PostUser]
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
    author: Union[str, PostUser]

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
    author: Union[str, PostUser]
    created: datetime
    post_id: int

    class Config:
        orm_mode = True

    @validator('author', always=True, pre=True)
    def validate_author_username(cls, v):
        return v.username


# Follow block
class FollowBase(BaseModel):
    pass


class FollowCreate(FollowBase):
    following_id: str = Field(alias='following')

    class Config:
        allow_population_by_field_name = True


class Follow(FollowBase):
    follows_id: int = Field(alias='id')
    user_id: Union[str, int] = Field(alias='user')
    following_id: Union[str, int] = Field(alias='following')

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

    @validator('user_id', always=True, pre=True)
    def validate_user_username(cls, v):
        user = get_user(SessionLocal(), v)
        return user.username

    @validator('following_id', always=True, pre=True)
    def validate_following_username(cls, v):
        following = get_user(SessionLocal(), v)
        return following.username
