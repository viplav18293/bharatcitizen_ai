# BharatAI Citizen Assistant Research

## Purpose
The research phase ensures all ingested content is from official Indian government sources (ending in `.gov.in` or `.nic.in`) and that the RAG pipeline is correctly configured for local, offline-capable indexing.

## Data Sourcing Strategy
- Only official domain-specific crawler connectors.
- Validation of source authority before ingestion.

## RAG Pipeline Research
- **Embeddings:** Local `all-MiniLM-L6-v2` validated for offline capability.
- **Retrieval:** Semantic search in ChromaDB.
- **Hallucination Mitigation:** Strict context-only prompting.
