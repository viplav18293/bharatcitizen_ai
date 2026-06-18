import asyncio
import os
import sys

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), "backend"))

from services.ingestion_service import ingestion_service
from core.config import settings

async def init_db():
    print("Initializing Database with sample data...")
    sample_file = "data/raw/aadhaar_info.txt"
    if os.path.exists(sample_file):
        result = await ingestion_service.ingest_local_file(
            file_path=sample_file,
            category="Aadhaar",
            source_url="https://uidai.gov.in"
        )
        print(f"Ingested: {result}")
    else:
        print(f"Sample file {sample_file} not found.")

if __name__ == "__main__":
    # Ensure environment variables are loaded
    if not settings.LLM_API_KEY or settings.LLM_API_KEY == "your-api-key":
        print("Error: LLM_API_KEY not set in backend/.env")
        sys.exit(1)
    
    asyncio.run(init_db())
