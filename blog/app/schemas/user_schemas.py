# from typing import List, Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


class PostUser(UserBase):
    username: str

    class Config:
        orm_mode = True


class UserInDB(User):
    hashed_password: str
    # Возможно не требуется. Разобраться.
