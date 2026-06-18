# AI Agents and Logic: BharatAI Citizen Assistant

This document provides a technical overview of the AI architecture and logic used in the BharatAI project.

## Retrieval-Augmented Generation (RAG) Architecture

BharatAI employs a robust RAG pipeline to ensure that all information provided to citizens is accurate, verifiable, and sourced from official government documents.

### Key Components

1.  **Orchestration**: Built with **LangChain**. LangChain manages the flow between user input, document retrieval, and the Final LLM synthesis.
2.  **Vector Database**: **ChromaDB** is used to store and index high-dimensional embeddings of official government documents.
3.  **Embeddings**: Uses **HuggingFace** models (e.g., `sentence-transformers/all-MiniLM-L6-v2`) for local, efficient semantic representation of text chunks.
4.  **LLM (Large Language Model)**: Integrates with **OpenAI** (or OpenAI-compatible APIs) for synthesizing final responses in natural language.

## The Logic Flow

1.  **Query Processing**: When a user asks a question, the query is embedded using the same embedding model used for the documents.
2.  **Semantic Search**: ChromaDB performs a similarity search to find the top $k$ relevant document chunks.
3.  **Source Verification**:
    -   The system filters retrieved documents based on an **Official Source Registry**.
    -   Only documents from verified domains (e.g., `.gov.in`, `.nic.in`) are passed to the synthesis stage.
4.  **Synthesis**:
    -   The LLM is provided with the retrieved official context and a strict system prompt.
    -   **Constraint**: If the answer is not in the context, the agent must state: "No verified information was found from official sources."
5.  **Transparency**:
    -   **Confidence Scores**: Calculated based on the similarity score from the vector database.
    -   **Citations**: The system extracts the source URL and title from metadata to provide direct links to users.

## Official Data Sources

BharatAI ingest data exclusively from official Indian government portals, including but not limited to:
-   **UIDAI** (`uidai.gov.in`): Aadhaar services.
-   **NTA** (`nta.ac.in`): National testing and exams.
-   **Passport Seva** (`passportindia.gov.in`): Passport applications.
-   **India Code** (`indiacode.nic.in`): Laws and regulations.
-   **PM Kisan** (`pmkisan.gov.in`): Agricultural schemes.
-   **Voter Service Portal** (`eci.gov.in`): Election Commission services.

## Multilingual Support
The agent is designed to handle queries in multiple Indian languages by utilizing the LLM's inherent multilingual capabilities and a dedicated translation layer in the frontend for UI elements.
