import uuid
from typing import Optional

from sqlmodel import SQLModel, Field


class Chat(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)


class Message(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False)

    chat_id: uuid.UUID = Field(foreign_key="chat.id", nullable=False)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)
    content: str
