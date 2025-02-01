from app.db.config import get_session
from app.repositories.chat_repository import ChatRepository
from app.services.rag_service import RAGService


def get_rag_service() -> RAGService:
    return RAGService()

def get_chat_repository() -> ChatRepository:
    with get_session() as session:
        yield ChatRepository(session)
