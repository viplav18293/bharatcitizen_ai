# Deployment

## Local Setup
1. Clone repository.
2. Create virtual environment: `python -m venv venv`.
3. Activate: `.\venv\Scripts\activate` (Windows).
4. Install requirements: `pip install -r backend/requirements.txt`.
5. Create `.env` file (see below).
6. Ingest data: `python backend/ingestion/production_ingest.py`.
7. Start backend: `python backend/main.py`.
8. Start frontend: `streamlit run app.py`.

## Environment Variables (.env)
```
LLM_API_KEY=your_key_here
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4o
EMBEDDING_MODEL=all-MiniLM-L6-v2
VECTOR_DB_TYPE=chroma
```

## Docker Setup
(Planned for production)
- `Dockerfile` included in backend for deployment.
