import uuid
from typing import Annotated

from fastapi import APIRouter, Depends

from app.dependencies import get_rag_service, get_chat_repository, get_message_repository, oauth2_scheme
from app.models.chat import Message, Chat, MessageType
from app.models.user import User
from app.repositories.chat_repository import ChatRepository
from app.repositories.message_repository import MessageRepository
from app.schemas.chat import MessageRequest, MessageResponse, ChatCreateResponse
from app.security.security_config import get_current_user
from app.services.rag_service import RAGService

router = APIRouter()


@router.post("/", response_model=ChatCreateResponse)
async def new_chat(chat_repository: ChatRepository = Depends(get_chat_repository), user: User = Depends(get_current_user)):
    chat = Chat(user_id=user.id)
    await chat_repository.create_chat(chat)
    return ChatCreateResponse(id=chat.id)


@router.post("/{chat_id}", response_model=MessageResponse)
async def new_message(
                      chat_id: uuid.UUID, message: MessageRequest,
                      rag_service: RAGService = Depends(get_rag_service),
                      message_repository: MessageRepository = Depends(get_message_repository),
                      user: User = Depends(get_current_user)):
    response_content = await __generate_response(chat_id, message, message_repository, rag_service, user)
    return MessageResponse(response=response_content)


@router.post("/{chat_id}/delete_last_user_message")
async def delete_last_user_message(
                                   chat_id: uuid.UUID,
                                   message_repository: MessageRepository = Depends(get_message_repository),
                                   user: User = Depends(get_current_user)):
    await message_repository.delete_last_user_message(chat_id, user.id)
    return {}

@router.post("/{chat_id}/update_last_user_message")
async def update_last_user_message(chat_id: uuid.UUID,
                                    message: MessageRequest,
                                    rag_service: RAGService = Depends(get_rag_service),
                                    message_repository: MessageRepository = Depends(get_message_repository),
                                    user: User = Depends(get_current_user)):
    await message_repository.handle_last_user_message_for_update(chat_id, user.id)
    response_content = await __generate_response(chat_id, message, message_repository, rag_service, user)
    return MessageResponse(response=response_content)



async def __generate_response(chat_id, message, message_repository, rag_service, user):
    context = await rag_service.query_knowledge_base(message.content)
    response_content = await rag_service.generate_response(message.content, context)
    user_message = Message(chat_id=chat_id, user_id=user.id, content=message.content, type=MessageType.USER)
    system_message = Message(chat_id=chat_id, user_id="123e4567-e89b-12d3-a456-426614174001", content=response_content, type=MessageType.SYSTEM)
    await message_repository.create_message(user_message)
    await message_repository.create_message(system_message)
    return response_content