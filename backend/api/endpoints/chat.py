from fastapi import APIRouter
from loguru import logger

from schemas.chat import ChatRequest, ChatResponse
from services.adk_agents import citizen_assistant_agent

router = APIRouter()

@router.post("", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    logger.info("POST /api/v1/chat received")
    return await citizen_assistant_agent.query(
        message=request.message,
        history=request.history,
        language=request.language,
        session_id=request.session_id,
    )
