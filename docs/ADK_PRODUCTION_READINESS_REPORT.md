# BharatAI ADK Production Readiness Report

## Backend Root Cause

The recurring `WinError 10061` happened because the FastAPI process was not listening on port `8000`.
Starting the app from the repository root with `python -m uvicorn backend.main:app` failed before binding because
`backend/main.py` imported `api`, `core`, and `services` as top-level modules without adding the backend directory
to `sys.path`.

The backend also performed heavy RAG imports and embedding initialization at module import time. On this local
Python 3.13 environment, the embedding dependency stack can hard-crash during import, so startup now binds first
and reports RAG state through health endpoints.

## Added Endpoints

- `GET /health`
- `GET /api/health`
- `GET /api/admin/system`
- `GET /admin/system`
- existing `GET /api/v1/admin/system`
- existing `POST /api/v1/chat`

## ADK Components Added

- `CitizenAssistantAgent`
- Aadhaar Agent
- PAN Agent
- Exam Agent
- Government Schemes Agent
- Rights & Law Agent
- Retrieval Agent

## ADK Tools Added

- `retrieve_documents()`
- `search_sources()`
- `get_scheme_information()`
- `get_exam_information()`
- `get_citizen_rights()`
- `portal_lookup()`
- `citation_validator()`

All tools call the existing RAG service and source validation logic.

## Source Safety

Only the approved official domains are accepted:

- `uidai.gov.in`
- `incometax.gov.in`
- `eci.gov.in`
- `passportindia.gov.in`
- `parivahan.gov.in`
- `digilocker.gov.in`
- `nta.ac.in`
- `upsc.gov.in`
- `pmkisan.gov.in`
- `nha.gov.in`
- `pmaymis.gov.in`
- `rtionline.gov.in`
- `indiacode.nic.in`
- `labour.gov.in`

## Startup Commands

Development:

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Repository-root compatible:

```bash
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

Production with explicit ADK and RAG initialization:

```bash
set GOOGLE_ADK_ENABLED=true
set RAG_BACKGROUND_INIT=true
set LLM_API_KEY=your-api-key
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

## Verification

```bash
pytest tests/test_adk_agents.py tests/test_backend_routes.py -q -p no:cacheprovider
```

Result: `9 passed`.

## Remaining Blockers

- No GitLab remote is configured locally. Add one before pushing to GitLab.
- Full live RAG initialization depends on a compatible Python/runtime dependency stack and local embedding model availability.
