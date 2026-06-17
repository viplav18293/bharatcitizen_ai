# RAG Architecture

BharatAI employs a robust, grounded RAG pipeline.

## Ingestion Pipeline
1. **Connector:** Domain-specific crawler (e.g., AadhaarConnector).
2. **Document Loading:** `WebBaseLoader` for official URLs.
3. **Chunking:** `RecursiveCharacterTextSplitter` (chunk_size: 1000, overlap: 200).
4. **Embedding:** Local `sentence-transformers/all-MiniLM-L6-v2`.
5. **Vector Storage:** Chroma (local persistence).

## Retrieval & Synthesis
1. **Query:** User input via FastAPI.
2. **Retrieval:** Semantic search using embedded query in ChromaDB.
3. **Re-ranking:** (Planned) Cross-encoder re-ranking.
4. **Synthesis:** Optional LLM synthesis (if API key present).
5. **Grounding:** Strict hallucination protection; context required for answer generation.
6. **Attribution:** Structured metadata output (Source, URL, Last Updated, Document Type).
7. **Confidence:** Scoring based on retrieval similarity.
