from sqlalchemy.orm import Session

from ..models import post_models as models
from ..schemas import post_schemas as schemas


# post_block
def get_post_list(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Post).offset(skip).limit(limit).all()


def get_single_post(db: Session, post_id: int):
    return db.query(models.Post).filter(models.Post.id == post_id).first()


def create_post(db: Session, post: schemas.PostCreate, author_id: int):
    # Реализовать добавление и апдейт группы
    db_post = models.Post(**post.dict(), author_id=author_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def update_post(db: Session, post: schemas.PostCreate, post_id: int):
    post_from_db = get_single_post(db, post_id)
    post_from_db.text = post.text  # Может не сработать
    db.commit()
    db.refresh(post_from_db)
    return post_from_db


def delete_post(db: Session, post_id: int):
    post_from_db = get_single_post(db, post_id)
    db.delete(post_from_db)
    db.commit()
    return post_from_db


# comment_block
def get_comment_list(
    db: Session, post_id: int, skip: int = 0, limit: int = 10
):
    return db.query(models.Comment).offset(skip).limit(limit).filter(
        post_id == post_id).all()


def get_single_comment(db: Session, post_id: int, comment_id: int):
    return db.query(models.Comment).filter(
        post_id == post_id, id == comment_id
    ).first()


def create_comment(
    db: Session, comment: schemas.CommentCreate, author_id: int, post_id: int
):
    db_comment = models.Comment(
        **comment.dict(), post_id=post_id, author_id=author_id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def comment_update(
    db: Session, comment: schemas.CommentCreate,
    post_id: int, comment_id: int
):
    comment_from_db = db.query(models.Comment).filter(
        post_id == post_id, comment_id == comment_id).first()
    # Проверить работу и заменить на вызов функции get_single_comment
    comment_from_db.text = comment.text
    db.commit()
    db.refresh(comment_from_db)
    return comment_from_db


def comment_delete(db: Session, post_id: int, comment_id: int):
    comment_from_db = get_single_comment(db, post_id, comment_id)
    db.delete(comment_from_db)
    db.commit()
    return comment_from_db


# group_block
def get_group_list(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Group).offset(skip).limit(limit).all()


def get_single_group(db: Session, group_id: int):
    return db.query(models.Group).filter(id == group_id).first()


def create_group(db: Session, group: schemas.GroupCreate):
    db_group = models.Group(**group)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group


def updete_group(db: Session, group: schemas.GroupCreate, group_id):
    group_from_db = get_single_group(db, group_id)
    group_from_db.title = group.title
    db.commit()
    db.refresh(group_from_db)
    return group_from_db


def delete_group(db: Session, group_id):
    group_from_db = get_single_group(db, group_id)
    db.delete(group_from_db)
    db.commit()
    return group_from_db


# follow_block
def get_following_list(
    db: Session, user_id: int, skip: int = 0, limit: int = 10
):
    return db.query(models.follow_table).offset(skip).limit(
        limit).filter(user_id == user_id).all()


def get_follower_list(
    db: Session, following_id: int, skip: int = 0, limit: int = 10
):
    return db.query(models.Follow).offset(skip).limit(
        limit).filter(following_id == following_id).all()


def get_single_follow(db: Session, user_id: int, following_id: int):
    return db.query(models.follow_table).filter(
        user_id == user_id, following_id == following_id
    ).first()


def create_follow(db: Session, follow: schemas.FollowCreate):
    db_follow = models.follow_table(**follow)
    db.add(db_follow)
    db.commit()
    db.refresh(db_follow)
    return db_follow


def delete_follow(db: Session, user_id: int, following_id: int):
    follow_from_db = get_single_follow(db, user_id, following_id)
    db.delete(follow_from_db)
    db.commit()
    return follow_from_db
