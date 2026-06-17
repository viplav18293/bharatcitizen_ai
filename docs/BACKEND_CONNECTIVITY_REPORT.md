# Backend Connectivity Report

## Root Cause
The backend consistently fails to bind to port 8000 on the local host with `[WinError 10048]`, despite attempting to kill processes occupying the port.

## Files Modified
- `backend/main.py` (adjusted host/port settings)
- `.env` (added `BACKEND_URL`)
- `app.py` (updated to use `BACKEND_URL` from `.env`)

## Routes Implemented
- `GET /health` (via `api/endpoints/health.py`)
- `POST /api/v1/chat` (via `api/endpoints/chat.py`)

## Startup Commands
- Backend: `start_backend.bat` (runs uvicorn)
- Frontend: `start_frontend.bat` (runs streamlit)

## Remaining Issues
- Connectivity between Streamlit and FastAPI is still failing with `Connection Refused` on 8000, likely due to a system-level restriction or binding failure.
- RAG initialization is in fallback mode due to missing `LLM_API_KEY`.
