import uuid

from fastapi import APIRouter, Depends

from app.dependencies import get_rag_service, get_chat_repository, get_message_repository
from app.models.chat import Message, Chat
from app.repositories.chat_repository import ChatRepository
from app.repositories.message_repository import MessageRepository
from app.schemas.chat import MessageRequest, MessageResponse, ChatCreateResponse
from app.services.rag_service import RAGService

router = APIRouter()


@router.post("/", response_model=ChatCreateResponse)
async def new_chat(chat_repository: ChatRepository = Depends(get_chat_repository)):
    chat = Chat(user_id='123e4567-e89b-12d3-a456-426614174000')
    await chat_repository.create_chat(chat)
    return ChatCreateResponse(id=chat.id)


@router.post("/{chat_id}", response_model=MessageResponse)
async def new_message(chat_id: uuid.UUID, message: MessageRequest,
                      rag_service: RAGService = Depends(get_rag_service),
                      message_repository: MessageRepository = Depends(get_message_repository)):
    context = await rag_service.query_knowledge_base(message.content)
    response_content = await rag_service.generate_response(message.content, context)
    user_message = Message(chat_id=chat_id, user_id="123e4567-e89b-12d3-a456-426614174000", content=message.content)
    system_message = Message(chat_id=chat_id, user_id="123e4567-e89b-12d3-a456-426614174001", content=response_content)
    await message_repository.create_message(user_message)
    await message_repository.create_message(system_message)
    return MessageResponse(response=response_content)
