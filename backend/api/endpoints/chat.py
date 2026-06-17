from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from services.rag_service import rag_service
from schemas.chat import Message, ChatResponse

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    history: List[Message] = []
    language: str = "en"

@router.post("", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    return await rag_service.query(request.message, request.history, request.language)
