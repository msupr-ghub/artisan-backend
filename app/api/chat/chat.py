import logging
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends

from app.dependencies import get_rag_service, get_chat_repository, get_message_repository, oauth2_scheme, \
    get_user_repository
from app.models.chat import Message, Chat, MessageType
from app.models.user import User
from app.repositories.chat_repository import ChatRepository
from app.repositories.message_repository import MessageRepository
from app.repositories.user_repository import UserRepository
from app.schemas.chat import MessageRequest, MessageResponse, ChatCreateResponse
from app.security.security_config import get_current_user
from app.services.rag_service import RAGService

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/", response_model=ChatCreateResponse)
async def new_chat(chat_repository: ChatRepository = Depends(get_chat_repository), user: User = Depends(get_current_user)):
    chat = Chat(user_id=user.id)
    await chat_repository.create_chat(chat)
    return ChatCreateResponse(id=chat.id)


@router.post("/{chat_id}/messages", response_model=MessageResponse)
async def new_message(
                      chat_id: uuid.UUID, message: MessageRequest,
                      rag_service: RAGService = Depends(get_rag_service),
                      message_repository: MessageRepository = Depends(get_message_repository),
                      user_repository: UserRepository = Depends(get_user_repository),
                      user: User = Depends(get_current_user)):
    system_user = await user_repository.get_system_user()
    response_message = await __generate_response(chat_id, message, message_repository, rag_service, user, system_user)
    return MessageResponse(response=response_message.content, created_at=response_message.created_at)


@router.post("/{chat_id}/messages/delete_last_user_message")
async def delete_last_user_message(
                                   chat_id: uuid.UUID,
                                   message_repository: MessageRepository = Depends(get_message_repository),
                                   user: User = Depends(get_current_user)):
    await message_repository.delete_last_user_message(chat_id, user.id)
    return {}

@router.post("/{chat_id}/messages/update_last_user_message")
async def update_last_user_message(chat_id: uuid.UUID,
                                    message: MessageRequest,
                                    rag_service: RAGService = Depends(get_rag_service),
                                    message_repository: MessageRepository = Depends(get_message_repository),
                                    user_repository: UserRepository = Depends(get_user_repository),
                                    user: User = Depends(get_current_user)):
    await message_repository.handle_last_user_message_for_update(chat_id, user.id)
    system_user = await user_repository.get_system_user()
    response_message = await __generate_response(chat_id, message, message_repository, rag_service, user, system_user)
    return MessageResponse(response=response_message.content, created_at=response_message.created_at)



async def __generate_response(chat_id: uuid.UUID,
                              message: MessageRequest,
                              message_repository: MessageRepository,
                              rag_service: RAGService,
                              user: User,
                              system_user: User
                              ) -> Message:
    context = await rag_service.query_knowledge_base(message.content)
    logger.info(f"Context: {context}")
    response_content = await rag_service.generate_response(message.content, context)
    user_message = Message(chat_id=chat_id, user_id=user.id, content=message.content, type=MessageType.USER)
    system_message = Message(chat_id=chat_id, user_id=uuid.UUID("123e4567-e89b-12d3-a456-426614174001"), content=response_content, type=MessageType.SYSTEM)
    await message_repository.create_message(user_message)
    await message_repository.create_message(system_message)
    return system_message