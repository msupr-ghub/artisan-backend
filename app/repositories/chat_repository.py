import uuid

from sqlmodel import Session

from app.models.chat import Chat

class ChatRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_chat(self, chat_id: uuid.UUID) -> Chat:
        return self.db.query(Chat).filter(Chat.id == chat_id).first()

    def get_chats(self, user_id: uuid.UUID) -> list[Chat]:
        return self.db.query(Chat).filter(Chat.user_id == user_id).all()

    def create_chat(self, chat: Chat) -> Chat:
        self.db.add(chat)
        self.db.commit()
        self.db.refresh(chat)
        return chat

    def update_chat(self, chat: Chat) -> Chat:
        self.db.merge(chat)
        self.db.commit()
        return chat

    def delete_chat(self, chat_id: uuid.UUID) -> None:
        chat = self.db.query(Chat).filter(Chat.id == chat_id).first()
        if chat:
            self.db.delete(chat)
            self.db.commit()