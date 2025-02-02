import uuid
from enum import Enum
from typing import Optional

from pydantic import EmailStr
from sqlmodel import SQLModel, Field

from app.models.mixins import TimestampsMixin

class UserType(Enum):
    SYSTEM = "system"
    USER = "user"
class User(SQLModel, TimestampsMixin, table=True):
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False)
    username: str
    email: str
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False
    user_type: UserType = UserType.USER