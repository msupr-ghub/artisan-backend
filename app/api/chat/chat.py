from fastapi import APIRouter

router = APIRouter()
@router.post("/chats")
async def new_chat():
    return "Chat created"
