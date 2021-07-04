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


class UserInDB(User):
    hashed_password: str
    # Возможно не требуется. Разобраться.
