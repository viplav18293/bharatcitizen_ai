import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "BharatAI Citizen Assistant"
    API_V1_STR: str = "/api/v1"
    
    # LLM Settings
    LLM_API_KEY: Optional[str] = None
    LLM_BASE_URL: str = "https://api.openai.com/v1"
    LLM_MODEL: str = "gpt-4o"
    
    # Embedding Settings
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    
    # Vector DB Settings
    VECTOR_DB_TYPE: str = "chroma"  # "chroma" or "qdrant"
    CHROMA_DB_PATH: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "chroma_db"))
    QDRANT_URL: Optional[str] = None
    QDRANT_API_KEY: Optional[str] = None
    QDRANT_COLLECTION: str = "bharatai_docs"
    
    LOG_LEVEL: str = "INFO"
    SIMILARITY_THRESHOLD: float = 0.35  # Minimum similarity score for retrieval

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")

settings = Settings()
