from typing import List
from uuid import UUID

from sqlmodel import Session

from app.models.chat import Message, MessageType


class MessageRepository:
    def __init__(self, session: Session):
        self.session = session

    async def get_messages(self, chat_id: int) -> List[Message]:
        return self.session.query(Message).filter(Message.chat_id == chat_id).all()

    async def create_message(self, message: Message) -> Message:
        self.session.add(message)
        self.session.commit()
        return message

    async def delete_message(self, message_id: int) -> None:
        message = self.session.query(Message).get(message_id)
        self.session.delete(message)
        self.session.commit()

    async def update_message(self, message_id: int, text: str) -> Message:
        message = self.session.query(Message).get(message_id)
        message.text = text
        self.session.commit()
        return message

    async def delete_last_user_message(self, chat_id: UUID, user_id: UUID) -> None:
        message = self.session.query(Message).filter(Message.chat_id == chat_id, Message.user_id == user_id).order_by(Message.created_at.desc()).first()
        self.session.delete(message)
        self.session.commit()

    async def delete_last_system_message(self, chat_id: UUID) -> None:
        message = self.session.query(Message).filter(Message.chat_id == chat_id, Message.type == MessageType.SYSTEM).order_by(Message.created_at.desc()).first()
        self.session.delete(message)
        self.session.commit()

    async def handle_last_user_message_for_update(self, chat_id: UUID, user_id: UUID) -> bool:
        # delete last system and user message, then a new message with new system response will be created
        try:
            await self.delete_last_system_message(chat_id)
            await self.delete_last_user_message(chat_id, user_id)
            return True
        except Exception as e:
            return False
