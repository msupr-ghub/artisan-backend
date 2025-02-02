import uuid
from datetime import datetime
from enum import Enum
from typing import Optional

from sqlmodel import SQLModel, Field

from app.models.mixins import TimestampsMixin


class Chat(SQLModel, TimestampsMixin, table=True):
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)

# enum message type, either system or user
class MessageType(Enum):
    SYSTEM = "system"
    USER = "user"

class Message(SQLModel, TimestampsMixin, table=True):
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False)

    chat_id: uuid.UUID = Field(foreign_key="chat.id", nullable=False)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)
    content: str
    type: MessageType
