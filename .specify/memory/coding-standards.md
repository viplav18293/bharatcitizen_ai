# Coding Standards

## Folder Structure
- `/backend`: FastAPI application and business logic.
- `/data`: Persistent data (Vector DB, local knowledge base).
- `/docs`: Project documentation and reports.
- `/scripts`: Utility scripts for maintenance and ingestion.
- `/pages`: Streamlit frontend pages.

## Naming Conventions
- Snake_case for Python modules and variables.
- PascalCase for classes.

## Logging
- Use `loguru` for structured, leveled logging.
- Log failures, initialization events, and retrieval stats.

## Error Handling
- Never expose raw tracebacks to users.
- Log full errors to backend; return user-friendly, non-hallucinated fallback messages if retrieval fails.

## RAG Rules
- **Source-first:** Answers must be synthesized from retrieved documents.
- **Attribution:** Every answer must include Title, URL, and Date of the source.
- **Hallucination Protection:** If context is insufficient, explicitly state information could not be verified.
