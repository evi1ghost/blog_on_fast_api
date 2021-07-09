from sqlalchemy.orm import Session

from ..models import post_models as models
from ..schemas import post_schemas as schemas
from .base import PostCRUDBase


class PostCRUD(PostCRUDBase[models.Post, schemas.PostCreateOrUpdate]):
    pass


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


def get_follower_list(
    db: Session, following_id: int, skip: int = 0, limit: int = 10
):
    return db.query(models.Follow).filter(
        models.Follow.following_id == following_id
        ).offset(skip).limit(limit).all()


def get_single_follow(db: Session, follow_id: int):
    return db.query(models.follow_table).filter(
        models.follow_table.id == follow_id
    ).first()


def create_follow(db: Session, follow: schemas.FollowCreate, user_id: int):
    db_follow = models.Follow(**follow.dict(), user_id=user_id)
    db.add(db_follow)
    db.commit()
    db.refresh(db_follow)
    return db_follow


def delete_follow(db: Session, user_id: int, following_id: int):
    follow_from_db = get_single_follow(db, user_id, following_id)
    db.delete(follow_from_db)
    db.commit()
    return follow_from_db
