from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..crud.post_crud import Group
from ..crud import user_crud
from ..models import user_models
from ..schemas import post_schemas


router = APIRouter(
    prefix='/group',
    tags=['Group']
)


@router.get('/', response_model=List[post_schemas.Group])
def read_group_list(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    return Group.get_list(db, skip, limit)


@router.get('/{group_id}/', response_model=post_schemas.Group)
def read_single_group(group_id: int, db: Session = Depends(get_db)):
    group = Group.get_single(db, group_id)
    if group is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Group not found'
        )
    return group


@router.post('/', response_model=post_schemas.Group, status_code=201)
def create_group(
    group: post_schemas.GroupCreateOrUpdate,
    db: Session = Depends(get_db),
    current_user: user_models.User = Depends(user_crud.get_current_active_user)
):
    return Group.create(db, group, current_user.id)


@router.patch('/{group_id}/', response_model=post_schemas.Group)
def update_group(
    group_id: int,
    group_update: post_schemas.GroupCreateOrUpdate,
    db: Session = Depends(get_db),
    current_user: user_models.User = Depends(user_crud.get_current_active_user)
):
    group = Group.get_single(db, group_id)
    if group is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Group not found'
        )
    if group.author != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Group can be changed only by author'
        )
    return Group.update(db, group, group_update)


@router.delete('/{group_id}/', status_code=204)
def delete_group(
    group_id: int,
    db: Session = Depends(get_db),
    current_user: user_models.User = Depends(user_crud.get_current_active_user)
):
    group = Group.get_single(db, group_id)
    if group is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Group not found'
        )
    if group.author != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Group can be deleted only by author'
        )
    return Group.delete(db, group)
