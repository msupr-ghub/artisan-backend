from uuid import UUID

from pydantic import BaseModel

from app.models.user import User

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

    def to_user(self) -> User:
        user = User()
        user.username = self.name
        user.email = self.email
        user.hashed_password = self.password
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