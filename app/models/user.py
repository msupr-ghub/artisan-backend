import uuid
from typing import Optional

from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
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