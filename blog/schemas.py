from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from .models import Post


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    posts: List[Post] = []

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    text: str
    pub_date: datetime


class PostCreate(BaseModel):
    pass


class Post(PostBase):
    id: int
    author_id: int
    group_id: int

    class Config:
        orm_mode = True
