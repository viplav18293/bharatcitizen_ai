from fastapi import UploadFile
from typing import List, Optional
import shutil
import os
from core.config import settings
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from loguru import logger

class IngestionService:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

    async def ingest_file(self, file: UploadFile, category: str, source_url: Optional[str] = None):
        # Save file to raw data
        os.makedirs("data/raw", exist_ok=True)
        file_path = f"data/raw/{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Load document
        if file.filename.endswith(".txt"):
            loader = TextLoader(file_path)
        elif file.filename.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        else:
            return {"error": "Unsupported file format"}

        documents = loader.load()
        
        # Add metadata
        for doc in documents:
            doc.metadata.update({
                "category": category,
                "source_url": source_url,
                "filename": file.filename
            })

        # Split into chunks
        chunks = self.text_splitter.split_documents(documents)
        
        # Store in ChromaDB
        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=settings.CHROMA_DB_PATH
        )
        
        logger.info(f"Ingested {len(chunks)} chunks from {file.filename}")
        return {"filename": file.filename, "chunks": len(chunks), "category": category}

    async def ingest_local_file(self, file_path: str, category: str, source_url: Optional[str] = None):
        # Load document
        if file_path.endswith(".txt"):
            loader = TextLoader(file_path)
        elif file_path.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        else:
            return {"error": "Unsupported file format"}

        documents = loader.load()
        
        # Add metadata
        for doc in documents:
            doc.metadata.update({
                "category": category,
                "source_url": source_url,
                "filename": os.path.basename(file_path)
            })

        # Split into chunks
        chunks = self.text_splitter.split_documents(documents)
        
        # Store in ChromaDB
        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=settings.CHROMA_DB_PATH
        )
        
        logger.info(f"Ingested {len(chunks)} chunks from {file_path}")
        return {"filename": os.path.basename(file_path), "chunks": len(chunks), "category": category}

ingestion_service = IngestionService()
