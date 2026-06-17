import os
from typing import List, Dict
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from services.rag_service import rag_service
from loguru import logger

class BaseConnector:
    def __init__(self, name: str, urls: List[str], category: str):
        self.name = name
        self.urls = urls
        self.category = category
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    def crawl(self) -> int:
        total_chunks = 0
        for url in self.urls:
            try:
                loader = WebBaseLoader(url)
                docs = loader.load()
                for doc in docs:
                    doc.metadata.update({
                        "source_url": url,
                        "category": self.category,
                        "source_name": self.name,
                        "document_type": "official_document"
                    })
                chunks = self.splitter.split_documents(docs)
                rag_service.vector_store.add_documents(chunks)
                total_chunks += len(chunks)
                logger.info(f"Ingested {len(chunks)} chunks from {url}")
            except Exception as e:
                logger.error(f"Failed to ingest {url}: {e}")
        return total_chunks
