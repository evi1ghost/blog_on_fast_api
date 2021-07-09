from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..crud import user_crud
from ..database import get_db
from ..schemas import user_schemas


router = APIRouter(
    tags=['Users']
)


@router.post('/users/', response_model=user_schemas.User, status_code=201)
def create_user(user: user_schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Username already registered'
        )
    return user_crud.create_user(db=db, user=user)
