from typing import List

from sqlmodel import Session

from app.models.chat import Message


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