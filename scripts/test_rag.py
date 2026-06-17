import os
import sys
import asyncio

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), "backend"))

from services.rag_service import rag_service
from loguru import logger

async def test_rag():
    logger.info("Starting RAG Validation Tests...")
    
    test_queries = [
        "How do I apply for Aadhaar?",
        "What are the fees for a PAN card?",
        "How to apply for Passport in India?",
        "What is PM Kisan scheme?",
        "How to file an RTI?",
        "What is the eligibility for UPSC?" # This should return "No verified information" or similar if not in DB
    ]
    
    for query in test_queries:
        logger.info(f"Testing Query: {query}")
        response = await rag_service.query(query, history=[])
        
        print(f"\nQUERY: {query}")
        print(f"ANSWER: {response.answer[:200]}...")
        print(f"CONFIDENCE: {response.confidence_score}")
        print(f"SOURCES: {[s.url for s in response.sources]}")
        
        if "No verified information" in response.answer and "UPSC" not in query:
            logger.error(f"FAIL: Expected information for '{query}' but got fallback response.")
        elif "UPSC" in query and "No verified information" in response.answer:
            logger.info(f"PASS: Correctly handled missing information for '{query}'.")
        else:
            logger.info(f"PASS: Received information for '{query}'.")

if __name__ == "__main__":
    # Ensure RAG is initialized
    if not rag_service.ready:
        logger.error("RAG Service not ready for testing.")
        sys.exit(1)
    asyncio.run(test_rag())
