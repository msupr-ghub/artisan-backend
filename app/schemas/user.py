from uuid import UUID

from bcrypt import hashpw, gensalt
from passlib.handlers.bcrypt import bcrypt
from pydantic import BaseModel

from app.models.user import User


class UserCreate(BaseModel):
    username: str
    email: str
    password: str

    def to_user(self) -> User:
        user = User()
        user.username = self.username
        user.email = self.email
        user.hashed_password = hashpw(self.password.encode('utf-8'), gensalt()).decode('utf-8')
        user.is_active = True
        user.is_superuser = False
        return user


class UserResponse(BaseModel):
    id: UUID
    username: str
    email: str
    is_active: bool
    is_superuser: bool

    @staticmethod
    def from_user(user: User):
        return UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
        )
