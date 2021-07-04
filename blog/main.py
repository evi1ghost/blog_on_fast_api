from datetime import timedelta

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.database import SessionLocal, engine, Base  # type: ignore
from app.crud import user_crud, post_crud  # type: ignore
from app.models import user_models, post_models  # type: ignore
from app.schemas import (  # type: ignore
    user_schemas, post_schemas, token_schemas
)
from app.auth import (  # type: ignore
    create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
)


app = FastAPI()


@app.post("/token", response_model=token_schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = user_crud.authenticate_user(
        SessionLocal, form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
