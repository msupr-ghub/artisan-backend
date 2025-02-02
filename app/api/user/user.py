from typing import Annotated

from fastapi import Depends, APIRouter
from sqlmodel import Session

from app.db.config import get_session
from app.dependencies import get_user_repository
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserResponse
from app.security.security_config import get_current_active_user

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate, user_repository: UserRepository = Depends(get_user_repository)):
    user = await user_repository.create(user.to_user())
    return UserResponse.from_user(user)

@router.get("/me", response_model=UserResponse)
async def read_users_me(
        current_user: Annotated[User, Depends(get_current_active_user)],
):
    return UserResponse.from_user(current_user)
