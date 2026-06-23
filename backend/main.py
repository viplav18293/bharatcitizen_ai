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

    logger.info("Starting BharatAI Citizen Assistant backend")
    logger.info(f"API prefix: {settings.API_V1_STR}")
    logger.info(f"Vector DB: {settings.VECTOR_DB_TYPE} at {settings.CHROMA_DB_PATH}")
    if settings.RAG_BACKGROUND_INIT:
        asyncio.create_task(asyncio.to_thread(rag_service.initialize_once))
        logger.info("RAG initialization scheduled in background")
    else:
        logger.warning("RAG background initialization disabled; set RAG_BACKGROUND_INIT=true to enable it")
    yield


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
    from services.adk_agents import citizen_assistant_agent
    from services.rag_service import rag_service

    rag_health = rag_service.get_health()
    return {
        "status": "ok" if rag_health.get("status") in {"online", "degraded"} else "degraded",
        "backend": True,
        "rag": rag_health,
        "adk": citizen_assistant_agent.get_status(),
    }

@app.get("/api/health")
async def api_health():
    return await root_health()

@app.get("/api/admin/system")
async def api_admin_system():
    from api.endpoints.admin import get_system_status

    return await get_system_status()

@app.get("/admin/system", response_class=HTMLResponse)
async def admin_system_dashboard():
    from api.endpoints.admin import get_system_status

    status = await get_system_status()
    adk = status.get("adk", {})
    rag = status.get("rag", {})
    api = status.get("api", {})
    rows = {
        "Backend Status": status.get("backend_status"),
        "ADK Status": adk.get("status"),
        "RAG Status": rag.get("status"),
        "Vector DB Status": rag.get("components", {}).get("vectordb"),
        "Document Count": rag.get("stats", {}).get("document_count"),
        "Agent Count": adk.get("agent_count"),
        "Memory Status": adk.get("memory_status"),
        "API Status": api.get("status"),
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
