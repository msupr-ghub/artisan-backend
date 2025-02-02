from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ChatCreateResponse(BaseModel):
    id: UUID

class MessageRequest(BaseModel):
    content: str

class MessageResponse(BaseModel):
    response: str
    created_at: datetime
