from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..crud.post_crud import Comment
from ..crud import user_crud
from ..models import user_models
from ..schemas import post_schemas


router = APIRouter(
    prefix='/posts/{post_id}/comments',
    tags=['Comments']
)


@router.get('/', response_model=List[post_schemas.Comment])
def read_comment_list(
    post_id: int,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    return Comment.get_list(db, skip, limit, post_id)


@router.get('/{comment_id}/', response_model=post_schemas.Comment)
def read_single_comment(
    post_id: int,
    comment_id: int,
    db: Session = Depends(get_db)
):
    comment = Comment.get_singl(db, comment_id, post_id)
    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Comment not found'
        )
    return comment


@router.post('/', response_model=post_schemas.Comment, status_code=201)
def create_comment(
    post_id: int,
    comment: post_schemas.CommentCreateOrUpdate,
    db: Session = Depends(get_db),
    current_user: user_models.User = Depends(user_crud.get_current_active_user)
):
    return Comment.create(db, comment, current_user.id, post_id)


@router.patch(
    '/{comment_id}/',
    response_model=post_schemas.Comment
)
def update_comment(
    post_id: int,
    comment_id: int,
    comment_update: post_schemas.CommentCreateOrUpdate,
    db: Session = Depends(get_db),
    current_user: user_models.User = Depends(user_crud.get_current_active_user)
):
    comment = Comment.get_singl(db, comment_id, post_id)
    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Comment not found'
        )
    if comment.author != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Comment can be changed only by author'
        )
    return Comment.update(db, comment, comment_update)


@router.delete('/{comment_id}/', status_code=204)
def delete_comment(
    post_id: int,
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: user_models.User = Depends(user_crud.get_current_active_user)
):
    comment = Comment.get_singl(db, comment_id, post_id)
    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Post not found'
        )
    if comment.author != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Comment can be deleted only by author'
        )
    return Comment.delete(db, comment)
