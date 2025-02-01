from fastapi import APIRouter, Depends

from app.dependencies import get_rag_service, get_chat_repository
from app.models.chat import Message
from app.repositories.chat_repository import ChatRepository
from app.schemas.chat import MessageRequest
from app.services.rag_service import RAGService

router = APIRouter()
@router.post("/")
async def new_chat():
    return "Chat created"

@router.post("/{chat_id}")
async def new_message(chat_id: int, message: MessageRequest,
                      rag_service: RAGService = Depends(get_rag_service),
                      chat_repository: ChatRepository = Depends(get_chat_repository)):
    context = await rag_service.query_knowledge_base(message.content)
    return await rag_service.generate_response(message.content, context=context)


