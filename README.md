# BharatAI Citizen Assistant

An AI-powered citizen copilot for India that helps users understand government services, schemes, exams, laws, rights, and official procedures using Retrieval-Augmented Generation (RAG).

## Features

- **Source-Backed Answers:** Every response is grounded in official government documents.
- **Official Portal Redirects:** Get direct links to official websites (UIDAI, NTA, Passport Seva, etc.).
- **Interactive Chat:** Modern, responsive conversational interface.
- **Multi-Domain Support:** MVP covers Aadhaar, PAN, Voter ID, Passport, NEET, JEE, UPSC, and more.
- **Trust Indicators:** Confidence scores and citation panels for transparency.

## Tech Stack

- **Backend:** FastAPI, LangChain, ChromaDB, OpenAI/OpenAI-compatible LLM.
- **Frontend:** Next.js 14, TypeScript, Tailwind CSS, Framer Motion, Lucide React.
- **RAG Pipeline:** Recursive Character Splitting, OpenAI Embeddings, Hybrid Retrieval.
- **Deployment:** Docker & Docker Compose.

## Getting Started

### Prerequisites

- Docker and Docker Compose
- OpenAI API Key (or any OpenAI-compatible API)

### Installation

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd citizenai_assistant
   ```

2. Set up environment variables:
   - Create a `backend/.env` file:
     ```env
     LLM_API_KEY=your-api-key
     LLM_BASE_URL=https://api.openai.com/v1
     LLM_MODEL=gpt-4o
     ```

3. Run with Docker Compose:
   ```bash
   docker-compose up --build
   ```

4. Initialize the database with sample data:
   ```bash
   python scripts/init_db.py
   ```

### Local Development (without Docker)

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate # or venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Data Sources

BharatAI ingest data from official sources only:
- [UIDAI](https://uidai.gov.in)
- [NTA](https://nta.ac.in)
- [Passport Seva](https://passportindia.gov.in)
- [India Code](https://indiacode.nic.in)
- [PM Kisan](https://pmkisan.gov.in)

## License

This project is for educational and civic-tech demonstration purposes. 
Official information should always be verified on government portals.
