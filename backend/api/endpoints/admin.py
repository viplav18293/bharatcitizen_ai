from fastapi import APIRouter
from services.rag_service import rag_service
from core.config import settings

router = APIRouter()

@router.get("/system")
async def get_system_status():
    health = rag_service.get_health()
    
    # Add extra admin info
    health.update({
        "environment": {
            "project_name": settings.PROJECT_NAME,
            "api_version": settings.API_V1_STR,
            "log_level": settings.LOG_LEVEL,
            "vector_db_path": settings.CHROMA_DB_PATH
        },
        "system_resources": {
            "status": "active",
            "mode": "production-ready" if health["status"] == "online" else "maintenance"
        }
    })
    
    return health

@router.get("/rag-status")
async def get_rag_status():
    return rag_service.get_rag_status()
