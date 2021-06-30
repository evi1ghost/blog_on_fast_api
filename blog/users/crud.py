from sqlalchemy.orm import Session

from ..auth import get_password_hash
from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filtre(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(
        models.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username, hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db.user)
    return db_user
