# Changelog

All notable changes to the **BharatAI Citizen Assistant** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-05-15 (Initial MVP)

### Added
- **Core RAG Pipeline**: Integrated LangChain and ChromaDB for retrieval-augmented generation.
- **FastAPI Backend**: Robust API with endpoints for chat, health checks, and data ingestion.
- **Streamlit Frontend**: Interactive conversational interface for Indian citizens.
- **Official Source Verification**: Logic to filter and prioritize information from `.gov.in` and `.nic.in` domains.
- **Multi-domain Support**: Initial data ingestion for Aadhaar, PAN, NEET, JEE, and Passport Seva.
- **Trust Indicators**: Confidence scores and direct links to official government portals.
- **Multilingual Foundation**: Initial support for English and Hindi queries.

### Fixed
- Improved retrieval accuracy by implementing recursive character splitting for large official documents.
- Resolved connection issues between the Streamlit frontend and FastAPI backend in Docker environments.

### Security
- Implemented environment variable management for LLM API keys.
- Added domain-level filtering to prevent the use of unofficial or misleading sources.
