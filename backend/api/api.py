from fastapi import APIRouter
from api.endpoints import ingestion, health, chat, admin

api_router = APIRouter()
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(ingestion.router, prefix="/ingestion", tags=["ingestion"])
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
