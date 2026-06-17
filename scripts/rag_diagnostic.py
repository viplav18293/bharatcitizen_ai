import os
import sys
import asyncio

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), "backend"))

from services.rag_service import rag_service
from core.config import settings
from loguru import logger

async def diagnostic_query(message: str):
    logger.info(f"--- Diagnostic Query: {message} ---")
    
    # 1. Direct Chroma search
    docs_with_scores = rag_service.vector_store.similarity_search_with_score(message, k=5)
    
    if not docs_with_scores:
        logger.error("Chroma returned 0 results!")
        return

    for doc, score in docs_with_scores:
        confidence = max(0, 1 - (score / 2.0))
        is_official = rag_service._is_official_source(doc.metadata.get("source_url"))
        
        status = "ACCEPTED" if (confidence >= settings.SIMILARITY_THRESHOLD and is_official) else "REJECTED"
        reason = []
        if confidence < settings.SIMILARITY_THRESHOLD:
            reason.append(f"Low confidence ({confidence:.4f} < {settings.SIMILARITY_THRESHOLD})")
        if not is_official:
            reason.append(f"Unofficial source ({doc.metadata.get('source_url')})")
            
        logger.info(f"[{status}] Score: {score:.4f} | Conf: {confidence:.4f} | URL: {doc.metadata.get('source_url')} | Reason: {', '.join(reason)}")
        logger.debug(f"Snippet: {doc.page_content[:100]}...")

    # 2. Call service.query
    response = await rag_service.query(message, [])
    logger.info(f"Final Answer: {response.answer[:100]}...")

if __name__ == "__main__":
    queries = ["pancard", "aadhaar card", "voter id", "passport", "pm kisan"]
    for q in queries:
        asyncio.run(diagnostic_query(q))
