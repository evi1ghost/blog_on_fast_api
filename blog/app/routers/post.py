from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..crud.post_crud import Post
from ..crud import user_crud
from ..models import user_models
from ..schemas import post_schemas


router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


@router.get('/', response_model=List[post_schemas.Post])
def read_post_list(
    skip: int = 0, limit: int = 10,
    db: Session = Depends(get_db),
    group: Optional[int] = None
):
    return Post.get_list(db, skip, limit, group)


@router.get('/{post_id}', response_model=post_schemas.Post)
def read_single_post(post_id: int, db: Session = Depends(get_db)):
    db_post = Post.get_single(db, post_id)
    if db_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Post not found'
        )
    return db_post


@router.post('/', response_model=post_schemas.Post, status_code=201)
def create_post(
    request_post: post_schemas.PostCreateOrUpdate,
    db: Session = Depends(get_db),
    current_user: user_models.User = Depends(user_crud.get_current_active_user)
):
    return Post.create(db, request_post, current_user.id)


@router.patch('/{post_id}/', response_model=post_schemas.Post)
def update_post(
    post_id: int,
    post_update: post_schemas.PostCreateOrUpdate,
    db: Session = Depends(get_db),
    current_user: user_models.User = Depends(user_crud.get_current_active_user)
):
    post = Post.get_single(db, post_id)
    if post.author != current_user:
        raise HTTPException(
            status_code=403, detail='Post can be changed only by author'
        )
    return Post.update(db, post, post_update)


@router.delete('/{post_id}/', status_code=204)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: user_models.User = Depends(user_crud.get_current_active_user)
):
    post = Post.get_single(db, post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Post not found'
        )
    if post.author != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Post can be deleted only by author'
        )
    return Post.delete(db, post)
