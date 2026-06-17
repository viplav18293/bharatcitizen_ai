import os
import sys

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), "backend"))

from services.rag_service import rag_service
from loguru import logger

def inspect_db():
    logger.info("Inspecting Vector Database...")
    if not rag_service.ready:
        logger.error("RAG Service not ready.")
        return

    collection = rag_service.vector_store._collection
    count = collection.count()
    logger.info(f"Total documents in collection: {count}")

    if count > 0:
        # Get all documents
        data = collection.get()
        ids = data['ids']
        metadatas = data['metadatas']
        documents = data['documents']

        for i in range(min(count, 20)):
            meta = metadatas[i]
            doc_snippet = documents[i][:100].replace('\n', ' ')
            source_url = meta.get('source_url', 'MISSING')
            logger.info(f"ID: {ids[i]} | URL: {source_url} | Content: {doc_snippet}...")

if __name__ == "__main__":
    inspect_db()
