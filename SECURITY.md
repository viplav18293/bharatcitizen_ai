# Security Policy

## Reporting a Vulnerability

We take the security of BharatAI Citizen Assistant seriously. If you believe you have found a security vulnerability, please report it to us as soon as possible.

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please send an email to `security@bharatai.org` (this is a placeholder, use the official project contact) with the following information:

- A description of the vulnerability.
- Steps to reproduce the issue.
- Potential impact.

We will acknowledge your report within 48 hours and provide a timeline for a fix.

## Scope

This security policy applies to:
- The FastAPI backend.
- The Streamlit frontend.
- The RAG ingestion scripts.
- Data handling and storage in ChromaDB.

## Best Practices

- **API Keys**: Never share your `LLM_API_KEY` or commit it to the repository. Use environment variables.
- **Data Privacy**: Ensure that no Personally Identifiable Information (PII) of citizens is stored in the vector database or logged in the backend.
- **Dependencies**: Keep your Python packages updated to avoid known vulnerabilities. Run `pip list --outdated` regularly.
