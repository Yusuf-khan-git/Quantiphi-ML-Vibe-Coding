from fastapi import APIRouter
from schemas import ChatRequest
from services.chat_service import process_chat_message

router = APIRouter(prefix="/api/chat", tags=["chat"])

@router.post("")
async def chat_endpoint(req: ChatRequest):
    result = await process_chat_message(req.message, req.userId)
    return result
