from fastapi import APIRouter
from services.rag_service import rag_service

router = APIRouter()

@router.get("/")
async def health_check():
    return rag_service.get_rag_status()
