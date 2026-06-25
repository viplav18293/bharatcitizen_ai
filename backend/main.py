import os
import sys
import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse

sys.path.insert(0, os.path.dirname(__file__))

from api.api import api_router
from core.config import settings
from loguru import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    from services.rag_service import rag_service
    from core.config import settings
    
    logger.info("Starting BharatAI Citizen Assistant backend")
    logger.info(f"API prefix: {settings.API_V1_STR}")
    logger.info(f"Vector DB: {settings.VECTOR_DB_TYPE} at {settings.CHROMA_DB_PATH}")
    
    if settings.RAG_BACKGROUND_INIT:
        task = asyncio.create_task(asyncio.to_thread(rag_service.initialize_once))
        task.add_done_callback(_log_background_task_result)
        logger.info("RAG initialization scheduled in background")
    else:
        logger.info("RAG background initialization disabled")
    yield


def _log_background_task_result(task: asyncio.Task):
    try:
        task.result()
    except asyncio.CancelledError:
        logger.warning("Background RAG initialization was cancelled")
    except Exception as exc:
        logger.exception(f"Background RAG initialization crashed: {exc}")


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled error on {request.method} {request.url.path}: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "message": "The backend caught an unexpected error. Check server logs for details.",
        },
    )

@app.get("/health")
async def root_health():
    from services.rag_service import rag_service

    rag_health = rag_service.get_health()
    components = rag_health.get("components", {})
    return {
        "status": "ok" if rag_health.get("status") in {"online", "degraded"} else "degraded",
        "backend": True,
        "llm": components.get("llm", False),
        "vectordb": components.get("vectordb", False),
        "embeddings": components.get("embeddings", False),
        "rag_ready": rag_health.get("status") == "online"
    }

@app.get("/api/health")
async def api_health():
    return await root_health()


@app.get("/api/admin/system")
async def legacy_api_admin_system():
    from api.endpoints.admin import get_system_status

    return await get_system_status()


@app.get("/admin/system", response_class=HTMLResponse)
async def admin_system_dashboard():
    from services.rag_service import rag_service
    from services.adk_agents import citizen_assistant_agent
    
    rag_status = rag_service.get_health()
    
    rows = {
        "Backend Status": "Online",
        "API Status": "Online",
        "LLM Status": "Connected" if rag_status["components"]["llm"] else "Disconnected",
        "Embedding Status": "Connected" if rag_status["components"]["embeddings"] else "Disconnected",
        "Vector DB Status": "Connected" if rag_status["components"]["vectordb"] else "Disconnected",
    }
    body = "".join(f"<tr><th>{key}</th><td>{value}</td></tr>" for key, value in rows.items())
    return f"""
    <!doctype html>
    <html>
      <head>
        <title>BharatAI System</title>
        <style>
          body {{ font-family: Arial, sans-serif; margin: 2rem; color: #172033; }}
          table {{ border-collapse: collapse; min-width: 520px; }}
          th, td {{ border: 1px solid #d7dde8; padding: 0.7rem 1rem; text-align: left; }}
          th {{ background: #eef3f8; }}
        </style>
      </head>
      <body>
        <h1>BharatAI System Dashboard</h1>
        <table>{body}</table>
      </body>
    </html>
    """


@app.get("/")
async def root():
    return {"message": "Welcome to BharatAI Citizen Assistant API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
