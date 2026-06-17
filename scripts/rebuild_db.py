import os
import sys
import shutil
import asyncio

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), "backend"))

from core.config import settings
from services.ingestion_service import ingestion_service
from loguru import logger

async def rebuild_db():
    logger.info("Starting database rebuild...")
    
    # 1. Clear existing database
    if os.path.exists(settings.CHROMA_DB_PATH):
        logger.info(f"Clearing existing database at {settings.CHROMA_DB_PATH}")
        shutil.rmtree(settings.CHROMA_DB_PATH)
    
    # 2. Ingest original Aadhaar file
    aadhaar_path = "data/raw/aadhaar_info.txt"
    if os.path.exists(aadhaar_path):
        await ingestion_service.ingest_local_file(
            aadhaar_path, 
            category="aadhaar", 
            source_url="https://uidai.gov.in"
        )

    # 3. Ingest new official documents
    official_dir = "data/raw/official"
    if os.path.exists(official_dir):
        for filename in os.listdir(official_dir):
            if filename.endswith(".txt"):
                file_path = os.path.join(official_dir, filename)
                category = filename.replace(".txt", "")
                
                # Simple logic to get URL from file content or mapping
                source_url = "https://india.gov.in"
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    for line in content.split("\n"):
                        if line.startswith("Official Portal:") or line.startswith("Sources:"):
                            source_url = line.split(":", 1)[1].strip()
                            break
                
                logger.info(f"Ingesting {filename} as {category} from {source_url}")
                await ingestion_service.ingest_local_file(
                    file_path,
                    category=category,
                    source_url=source_url
                )

    logger.info("Database rebuild complete.")

if __name__ == "__main__":
    asyncio.run(rebuild_db())
