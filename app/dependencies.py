from fastapi.security import OAuth2PasswordBearer

from app.db.config import get_session
from app.repositories.chat_repository import ChatRepository
from app.repositories.message_repository import MessageRepository
from app.repositories.user_repository import UserRepository
from app.services.rag_service import RAGService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_rag_service() -> RAGService:
    return RAGService()

def get_chat_repository() -> ChatRepository:
    with get_session() as session:
        yield ChatRepository(session)

def get_message_repository() -> MessageRepository:
    with get_session() as session:
        yield MessageRepository(session)

def get_user_repository() -> UserRepository:
    with get_session() as session:
        yield UserRepository(session)
