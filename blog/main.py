from datetime import timedelta

from fastapi import FastAPI
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from .app.auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from .app.crud import user_crud
from .app.database import get_db
from .app.routers import comments, follow, group, post, users
from .app.schemas import token_schemas


app = FastAPI()


PREFIX = '/api/v1'


app.include_router(users.router, prefix=PREFIX)
app.include_router(post.router, prefix=PREFIX)
app.include_router(comments.router, prefix=PREFIX)
app.include_router(group.router, prefix=PREFIX)
app.include_router(follow.router, prefix=PREFIX)


@app.post('/token/', response_model=token_schemas.Token, tags=['Users'])
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = user_crud.authenticate_user(
        db, form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': user.username}, expires_delta=access_token_expires
    )
    return {'access_token': access_token, 'token_type': 'bearer'}
