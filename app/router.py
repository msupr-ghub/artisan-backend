from fastapi import APIRouter
from app.api.chat.chat import router as chat_router
from app.api.user.user import router as user_router
from app.api.auth.auth import router as auth_router

api_router = APIRouter()


api_router.include_router(chat_router, prefix="/chats", tags=["Chat"])
api_router.include_router(user_router, prefix="/users", tags=["User"])