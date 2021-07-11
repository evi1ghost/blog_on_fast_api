from typing import Optional

from sqlalchemy.orm import Session

from ..models import post_models as models
from ..schemas import post_schemas as schemas
from .base import PostCRUDBase


class PostCRUD(PostCRUDBase[models.Post, schemas.PostCreateOrUpdate]):
    def get_list(
        self, db: Session, skip: int,
        limit: int, group_id: Optional[int] = None
    ):
        if group_id:
            return db.query(self.model).filter(
                self.model.group_id == group_id
            ).offset(skip).limit(limit).all()
        return db.query(self.model).offset(skip).limit(limit).all()


class CommentCRUD(
    PostCRUDBase[models.Comment, schemas.CommentCreateOrUpdate]
):
    pass


class GroupCRUD(PostCRUDBase[models.Group, schemas.GroupCreateOrUpdate]):
    pass


Post = PostCRUD(models.Post)
Comment = CommentCRUD(models.Comment)
Group = GroupCRUD(models.Group)


# follow block
def get_following_list(
    db: Session, user_id: int, skip: int = 0, limit: int = 10
):
    return db.query(models.Follow).filter(
        models.Follow.user_id == user_id
        ).offset(skip).limit(limit).all()


def get_follow_by_user_and_following_id(
    db: Session, following_id: int, user_id: int
):
    return db.query(models.Follow).filter(
        models.Follow.following_id == following_id,
        models.Follow.user_id == user_id
        ).first()


def get_single_follow(db: Session, id: int):
    return db.query(models.Follow).filter(
        models.Follow.follows_id == id).first()


def create_follow(db: Session, following_id: int, user_id: int):
    db_follow = models.Follow(following_id=following_id, user_id=user_id)
    db.add(db_follow)
    db.commit()
    db.refresh(db_follow)
    return db_follow


def delete_follow(db: Session, follow: models.Follow):
    db.delete(follow)
    db.commit()
    return follow
