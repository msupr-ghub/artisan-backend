import uuid
from typing import Optional

from sqlmodel import SQLModel, Field


class Chat(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False)


class Message(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False)

    chat_id: uuid.UUID = Field(foreign_key="Chat.id", nullable=False)
    user_id: uuid.UUID = Field(foreign_key="User.id", nullable=False)
