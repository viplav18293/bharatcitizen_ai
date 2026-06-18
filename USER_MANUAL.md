# BharatAI Citizen Assistant - User Manual

Welcome to the BharatAI Citizen Assistant! This guide will help you set up and use the application effectively.

## Table of Contents
1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Using the Streamlit Frontend](#using-the-streamlit-frontend)
4. [Using the Backend API](#using-the-backend-api)
5. [Troubleshooting](#troubleshooting)

---

## Introduction
BharatAI is an AI-powered copilot designed to help Indian citizens navigate government services, schemes, and official procedures. It uses Retrieval-Augmented Generation (RAG) to ensure every answer is grounded in official documentation.

## Getting Started

### Prerequisites
- Python 3.9+
- Docker & Docker Compose (optional, for containerized setup)
- An OpenAI-compatible API Key

### Quick Start
1. **Start the Backend**:
   - Navigate to `backend/`.
   - Install dependencies: `pip install -r requirements.txt`.
   - Create a `.env` file with your `LLM_API_KEY`.
   - Run: `uvicorn main:app --reload`.
2. **Start the Frontend**:
   - From the root directory, run: `streamlit run app.py`.

## Using the Streamlit Frontend
The frontend provides a user-friendly chat interface.

### Features
- **Language Selection**: Use the sidebar to switch between supported languages (English, Hindi, etc.).
- **Interactive Chat**: Type your query in the input box at the bottom (e.g., "How do I apply for a new PAN card?").
- **Official Links**: The sidebar contains quick links to major government portals like UIDAI, NTA, and Passport Seva.
- **Source Verification**: When the assistant provides an answer, it may also provide a "Visit Official Portal" button to take you directly to the verified source.

### Interaction Tips
- Be specific with your questions to get better results.
- Look for the "Trust Indicators" (Confidence scores) to understand the reliability of the response.

## Using the Backend API
Developers can interact directly with the FastAPI backend.

### Main Endpoint: `/api/v1/chat`
- **Method**: `POST`
- **Payload**:
  ```json
  {
    "message": "What are the eligibility criteria for PM Kisan?",
    "history": [],
    "language": "en"
  }
  ```
- **Response**: Returns a JSON object containing the `answer`, `sources`, `confidence_score`, and `official_portal_link`.

### Other Endpoints
- **Health Check**: `GET /api/v1/health` - Check the status of the RAG pipeline and vector database.
- **Admin**: `GET /api/v1/admin` - Access administrative stats.

## Troubleshooting
- **Backend Connection Error**: Ensure the FastAPI server is running on `http://localhost:8000`. You can change this in `app.py` or by setting the `BACKEND_URL` environment variable.
- **No Answers Found**: If the assistant says "No verified information was found", it means the query didn't match any official documents in the current database.
- **LLM Errors**: Verify your API key and base URL in `backend/.env`.
