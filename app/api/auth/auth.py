import os
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.config_vars import ACCESS_TOKEN_EXPIRE_MINUTES
from app.dependencies import get_user_repository
from app.models.user import User
from app.schemas.auth import Token
from app.schemas.user import UserResponse
from app.security.security_config import get_current_active_user, verify_password, \
    create_access_token

router = APIRouter()


@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                user_repository=Depends(get_user_repository)):
    user = await user_repository.get_by_username(form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not verify_password(form_data.password, user.hashed_password):
        return HTTPException(status_code=400, detail=f"Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

