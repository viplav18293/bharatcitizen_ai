from fastapi import APIRouter
from services.rag_service import rag_service
from core.config import settings
from services.adk_agents import citizen_assistant_agent

router = APIRouter()

@router.get("/system")
async def get_system_status():
    rag_health = rag_service.get_health()
    rag_status = rag_service.get_rag_status()
    adk_status = citizen_assistant_agent.get_status()
    
    return {
        "backend_status": "online",
        "adk": adk_status,
        "rag": rag_health,
        "vector_db": {
            "type": settings.VECTOR_DB_TYPE,
            "path": settings.CHROMA_DB_PATH,
            "status": rag_health.get("components", {}).get("vectordb", False),
            "document_count": rag_health.get("stats", {}).get("document_count", 0),
        },
        "documents": {
            "count": rag_status.get("documents", 0),
            "chunks": rag_status.get("chunks", 0),
            "collections": rag_status.get("collections", []),
        },
        "api": {
            "status": "online",
            "routes": [
                "GET /health",
                "GET /api/health",
                "GET /api/admin/system",
                "GET /admin/system",
                "GET /api/v1/admin/system",
                "POST /api/v1/chat",
            ],
        },
        "environment": {
            "project_name": settings.PROJECT_NAME,
            "api_version": settings.API_V1_STR,
            "log_level": settings.LOG_LEVEL,
            "vector_db_path": settings.CHROMA_DB_PATH
        },
        "system_resources": {
            "status": "active",
            "mode": "production-ready" if rag_health.get("status") == "online" else "maintenance"
        },
    }

@router.get("/rag-status")
async def get_rag_status():
    return rag_service.get_rag_status()
