# Architecture

BharatAI follows a decoupled RAG architecture designed for reliability and offline retrieval capability.

## Components
- **Frontend:** Streamlit for an interactive, data-centric UI.
- **Backend:** FastAPI for high-performance API services.
- **Vector DB:** Chroma (Local persistent) for document storage.
- **Embeddings:** `sentence-transformers/all-MiniLM-L6-v2` (Local).
- **Retrieval:** Hybrid search capabilities with dense vector retrieval.
- **Re-ranking:** Cross-encoder capability (to be added for production).
- **LLM:** Support for OpenAI-compatible providers (for synthesis).
- **Admin Management:** Dedicated ingestion service for source management, monitoring, and analytics.
