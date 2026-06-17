import os
import sys
import asyncio
from typing import List, Dict

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), "backend"))

from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from services.rag_service import rag_service
from loguru import logger

# Expanded Official Source URLs (Phase 5)
OFFICIAL_SOURCES = {
    "aadhaar": "https://uidai.gov.in/en/my-aadhaar/about-your-aadhaar.html",
    "pan": "https://www.incometax.gov.in/iec/foportal/help/permanent-account-number",
    "passport": "https://www.passportindia.gov.in/AppOnlineProject/welcomeLink",
    "voter_id": "https://eci.gov.in/voters/voter-electronic-guide-epic/",
    "driving_license": "https://parivahan.gov.in/parivahan//en/content/driving-licence-0",
    "pm_kisan": "https://pmkisan.gov.in/About.aspx",
    "rti": "https://rtionline.gov.in/about-us.php",
    "digilocker": "https://www.digilocker.gov.in/about/faq",
    "ayushman_bharat": "https://nha.gov.in/PM-JAY",
    "pm_awas": "https://pmaymis.gov.in/StaticPages/About_PMAY_U.aspx",
    "labour_rights": "https://labour.gov.in/policies/labour-laws",
    "consumer_rights": "https://consumerhelpline.gov.in/consumer-rights.php"
}

async def ingest_official_sources():
    logger.info("Starting Web Ingestion from Official Sources...")
    
    if not rag_service.ready:
        logger.error("RAG Service not ready for ingestion.")
        return

    documents = []
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=200)
    
    for category, url in OFFICIAL_SOURCES.items():
        try:
            logger.info(f"Ingesting: {url} ({category})")
            loader = WebBaseLoader(url)
            # Some sites might block standard requests, using simple loader for now
            docs = loader.load()
            for doc in docs:
                doc.metadata["source_url"] = url
                doc.metadata["category"] = category
                doc.metadata["title"] = f"Official {category.replace('_', ' ').title()} Information"
            
            chunks = text_splitter.split_documents(docs)
            documents.extend(chunks)
            logger.info(f"Successfully processed {len(chunks)} chunks from {url}")
        except Exception as e:
            logger.error(f"Error ingesting {url}: {e}")
            
    if documents:
        # Add to vector store
        rag_service.vector_store.add_documents(documents)
        logger.info(f"Total newly ingested chunks: {len(documents)}")
    else:
        logger.warning("No new documents were ingested.")

if __name__ == "__main__":
    asyncio.run(ingest_official_sources())
